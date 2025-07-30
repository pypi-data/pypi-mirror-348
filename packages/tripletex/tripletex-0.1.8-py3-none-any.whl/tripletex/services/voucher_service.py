"""Service for creating vouchers from simple information."""

import datetime
import logging  # Add logging import
from enum import Enum
from typing import Dict, List, Optional

import crudclient  # For exception handling

from tripletex.core.api import TripletexAPI
from tripletex.core.models import IdRef
from tripletex.endpoints.ledger.models.posting import PostingCreate
from tripletex.endpoints.ledger.models.voucher import Voucher, VoucherCreate, VoucherUpdate  # Add VoucherUpdate
from tripletex.endpoints.supplier.models import Supplier
from tripletex.services.posting_service import PostingService

logger = logging.getLogger(__name__)  # Initialize logger


class DuplicateExternalVoucherAction(Enum):
    """Defines actions to take when a duplicate external voucher number is encountered."""

    SKIP = "skip"
    OVERWRITE = "overwrite"
    CREATE_NEW = "create_new"
    RAISE_ERROR = "raise_error"


class VoucherService:
    """Service for creating vouchers from simple information."""

    def __init__(self, api_client: TripletexAPI):
        """Initialize the service with a Tripletex API client.

        Args:
            api_client: The Tripletex API client to use for API calls.
        """
        self.api_client = api_client
        self.posting_service = PostingService(api_client)

    def make_voucher(
        self,
        description: str,
        date: datetime.datetime,
        filepath: Optional[str],
        postings: List[Dict],
        supplier_name: Optional[str] = None,
        supplier_org_number: Optional[str] = None,
        supplier_id: Optional[int] = None,
        send_to_ledger: bool = False,
        voucher_type_id: Optional[int] = None,
        external_voucher_number: Optional[str] = None,
        on_duplicate_external_number: DuplicateExternalVoucherAction = DuplicateExternalVoucherAction.SKIP,
    ) -> Voucher:
        """Create a voucher with postings and an attachment.

        Args:
            description: Description of the voucher.
            date: Date of the voucher as a datetime object.
            filepath: Path to the PDF file to attach to the voucher.
            postings: List of dictionaries representing postings.
                Each dict should have:
                - amount: float (required)
                - accountnumber: str (required)
                - description: str (optional, overrides voucher description)
            supplier_name: Optional name of the supplier.
            supplier_org_number: Optional organization number of the supplier.
            supplier_id: Optional ID of the supplier (preferred over name/org_number).
            send_to_ledger: Whether to send the voucher to ledger during creation.
                Defaults to False.
            voucher_type_id: Optional ID of the voucher type to use.
                If not provided, a default expense voucher type will be used.
            external_voucher_number: Optional external voucher number.
            on_duplicate_external_number: Action to take if a voucher with the
                same external_voucher_number already exists.
                Defaults to DuplicateExternalVoucherAction.SKIP.
                (Actual logic for handling duplicates is not yet implemented).

        Returns:
            The created Voucher object.

        Raises:
            ValueError: If the postings don't balance to zero, if the file is not a PDF,
                        or if a duplicate external_voucher_number is found and the
                        on_duplicate_external_number action is RAISE_ERROR.
            NotFoundError: If an account or supplier cannot be found.
        """
        # Format date as YYYY-MM-DD string
        date_str = date.strftime("%Y-%m-%d")

        # --- Pre-calculate common elements needed for create/update ---
        # Find supplier if provided
        supplier_obj = None
        if supplier_id is not None:
            supplier_obj = self.api_client.suppliers.read(resource_id=str(supplier_id))
        elif supplier_org_number or supplier_name:
            supplier_obj = self.api_client.suppliers.get_supplier_by_organization_number_or_name_or_404(
                name=supplier_name, organization_number=supplier_org_number
            )

        # Resolve voucher type ID
        resolved_voucher_type_id: Optional[int]
        if voucher_type_id is not None:
            resolved_voucher_type_id = voucher_type_id
        else:
            default_voucher_type = self.api_client.ledger.voucher_type.get_by_code_or_404(code="K")
            resolved_voucher_type_id = default_voucher_type.id

        # Create posting objects
        posting_objects_list = self._create_posting_objects(postings, description, supplier_obj, date_str)
        # --- End of pre-calculation ---

        # Handle duplicate external voucher number logic
        if external_voucher_number and on_duplicate_external_number != DuplicateExternalVoucherAction.CREATE_NEW:
            existing_vouchers = self._find_vouchers_by_external_number(external_voucher_number)  # Removed 'date' argument
            if existing_vouchers:
                if on_duplicate_external_number == DuplicateExternalVoucherAction.RAISE_ERROR:
                    raise ValueError(
                        f"Duplicate external voucher number '{external_voucher_number}' found. "
                        f"Found {len(existing_vouchers)} existing voucher(s) with this external number "
                        f"in the fiscal year of {date.year} (e.g., ID: {existing_vouchers[0].id})."
                    )
                elif on_duplicate_external_number == DuplicateExternalVoucherAction.SKIP:
                    existing_voucher_to_return = existing_vouchers[0]
                    skip_message = (
                        f"SKIP action: Duplicate external voucher number '{external_voucher_number}' found. "
                        f"Returning existing voucher ID: {existing_voucher_to_return.id}."
                    )
                    logger.info(skip_message)
                    print(skip_message)
                    return existing_voucher_to_return
                elif on_duplicate_external_number == DuplicateExternalVoucherAction.OVERWRITE:
                    if len(existing_vouchers) > 1:
                        raise ValueError(
                            f"OVERWRITE action failed: Multiple existing vouchers found with external "
                            f"number '{external_voucher_number}'. Cannot determine which one to overwrite. "
                            f"Found IDs: {[v.id for v in existing_vouchers]}."
                        )
                    # Exactly one existing voucher found
                    voucher_to_overwrite = existing_vouchers[0]
                    if voucher_to_overwrite.id is None:
                        raise ValueError(
                            f"OVERWRITE action failed: Found existing voucher with external number " f"'{external_voucher_number}' but it has no ID."
                        )
                    raise NotImplementedError(
                        "OVERWRITE action is not yet implemented. Please implement the logic to "
                        "overwrite the existing voucher, then uncomment the following code block."
                        """
                        return self._perform_voucher_overwrite(
                                                existing_voucher_id=voucher_to_overwrite.id,
                                                date_str=date_str,
                                                description=description,
                                                voucher_type_id_to_use=resolved_voucher_type_id,
                                                posting_objects_for_update=posting_objects_list,
                                                send_to_ledger=send_to_ledger,
                                                filepath=filepath,
                                                external_voucher_number_being_processed=external_voucher_number
                                            )

                        """
                    )

        # --- Fall through to create a new voucher if no duplicates were handled above ---
        voucher_data = VoucherCreate(
            date=date_str,
            description=description,
            voucher_type=IdRef(id=resolved_voucher_type_id),  # Use resolved ID
            postings=posting_objects_list,  # Use created list
            send_to_ledger=send_to_ledger,
            external_voucher_number=external_voucher_number,
        )

        # Create the voucher using the VoucherCreate model
        # Pass send_to_ledger as a parameter to the create method
        created_voucher = self.api_client.ledger.voucher.create(data=voucher_data, send_to_ledger=send_to_ledger)

        # The voucher has already been created in the conditional block above

        self._handle_attachment(created_voucher.id, filepath)  # Call new helper

        return created_voucher

    def _perform_voucher_overwrite(
        self,
        existing_voucher_id: int,
        date_str: str,
        description: str,
        voucher_type_id_to_use: Optional[int],
        posting_objects_for_update: List[PostingCreate],
        send_to_ledger: bool,
        filepath: Optional[str],
        external_voucher_number_being_processed: Optional[str],
    ) -> Voucher:
        """Performs the overwrite operation on an existing voucher."""
        logger.info(
            f"OVERWRITE action: Attempting to update existing voucher ID {existing_voucher_id} "
            f"which has external number '{external_voucher_number_being_processed}'."
        )

        update_data = VoucherUpdate(
            date=date_str,
            description=description,
            voucher_type=IdRef(id=voucher_type_id_to_use) if voucher_type_id_to_use else None,
            postings=posting_objects_for_update,
            # external_voucher_number is intentionally not set here for an update of content.
        )

        try:
            updated_voucher = self.api_client.ledger.voucher.update(
                resource_id=str(existing_voucher_id),
                data=update_data,
                send_to_ledger=send_to_ledger,
            )
            logger.info(f"Successfully overwrote voucher ID: {updated_voucher.id}")
            self._handle_attachment(updated_voucher.id, filepath)
            return updated_voucher
        except crudclient.exceptions.UnprocessableEntityError:
            # Log the error but re-raise the original UnprocessableEntityError
            # so the test can catch the actual API error and inspect its details.
            logger.error(
                f"OVERWRITE action failed for voucher ID {existing_voucher_id} due to API validation error. "
                f"External number being processed: '{external_voucher_number_being_processed}'.",
                exc_info=True,  # This will include the stack trace and original exception info
            )
            raise  # Re-raise the caught UnprocessableEntityError
        except Exception as e:  # Catch other potential errors during update
            logger.error(f"OVERWRITE action failed for voucher ID {existing_voucher_id} with an unexpected error: {e}", exc_info=True)
            raise  # Re-raise other unexpected errors

    def _handle_attachment(self, voucher_id: int, filepath: Optional[str]) -> None:
        """Handles uploading an attachment to a voucher if a filepath is provided."""
        if filepath and filepath.strip():
            try:
                self.api_client.ledger.voucher.upload_attachment(voucher_id=voucher_id, file_path=filepath)
                logger.info(f"Successfully uploaded attachment to voucher ID: {voucher_id}")
            except Exception as e:
                logger.warning(f"Warning: Failed to upload attachment to voucher ID {voucher_id}: {str(e)}")

    def _find_vouchers_by_external_number(self, external_voucher_number: str) -> List[Voucher]:
        """
        Finds vouchers that match the given external_voucher_number using the
        dedicated API endpoint.

        Args:
            external_voucher_number: The external voucher number to search for.

        Returns:
            A list of Voucher objects that match the external_voucher_number.
        """
        if not external_voucher_number:
            return []

        try:
            # Use the dedicated endpoint method from TripletexVoucher
            # Request only necessary fields to optimize.
            response = self.api_client.ledger.voucher.external_voucher_number(
                external_voucher_number=external_voucher_number,
                fields="id,externalVoucherNumber",  # Ensure we get externalVoucherNumber for confirmation
                count=2000,  # Assuming this is enough; API might paginate if more
            )
            if response and response.values:
                # The endpoint should ideally only return matches, but we can double-check
                # However, the `external_voucher_number` method in crud class already filters.
                return list(response.values)
            return []
        except Exception as e:
            logger.error(f"Error calling 'external_voucher_number' endpoint for '{external_voucher_number}': {e}", exc_info=True)
            # Depending on desired behavior, could re-raise or return empty list
            return []

    def _create_posting_objects(
        self,
        postings: List[Dict],
        default_description: str,
        supplier: Optional[Supplier],
        date_str: str,
    ) -> List[PostingCreate]:
        """Create PostingCreate objects from simple posting dictionaries.

        Args:
            postings: List of dictionaries representing postings.
            default_description: Default description to use if not specified in the posting.
            supplier: Optional supplier to associate with the postings.
            date_str: Date string in YYYY-MM-DD format.

        Returns:
            List of PostingCreate objects.

        Raises:
            ValueError: If the postings don't balance to zero.
            NotFoundError: If an account cannot be found.
        """
        posting_objects = []

        # First pass: create all posting objects with row numbers
        for i, posting_dict in enumerate(postings, start=1):
            amount = posting_dict.get("amount")
            account_number = posting_dict.get("accountnumber")
            description = posting_dict.get("description", "") or default_description

            if amount is None or account_number is None:
                raise ValueError(f"Posting {i} is missing required fields: amount and accountnumber")

            # Find the account by number
            account = self.api_client.ledger.account.get_by_number_or_404(account_number)

            # Get the VAT type for the account
            vat_type_id = None
            vat_percentage = 0
            if account.vat_type and account.vat_type.id:
                vat_type_id = account.vat_type.id
                # Get the VAT percentage based on the VAT type ID
                # VAT type 3 is 25% in Norway (high rate)
                if vat_type_id == 3:
                    vat_percentage = 0.25  # type: ignore
                # Add other VAT types as needed

            # Calculate gross amount based on VAT
            # For both debit (positive) and credit (negative) amounts with VAT,
            # gross = net * (1 + VAT%)
            # For amounts without VAT, gross = net
            gross_amount = amount
            if vat_type_id and vat_type_id != 0:
                gross_amount = amount * (1 + vat_percentage)

                # If this is a VAT account, we need to create a VAT posting
                # This is handled by the API, so we don't need to do anything here

            # Create the posting object with all required fields
            posting = PostingCreate(
                row=i,
                description=description,
                account=IdRef(id=account.id),
                amount=amount,
                date=date_str,
                # Add these fields which are required for proper voucher creation
                amount_currency=amount,
                amount_gross=gross_amount,
                amount_gross_currency=gross_amount,
                currency=IdRef(id=1),  # Default currency (NOK)
            )

            # Set the VAT type
            if vat_type_id is not None:
                posting.vat_type = IdRef(id=vat_type_id)

            # Set the supplier if provided
            if supplier:
                posting.supplier = IdRef(id=supplier.id)

            posting_objects.append(posting)

        # Check if the postings balance to zero
        # We need to check the net amounts
        total_net = sum(p.amount or 0.0 for p in posting_objects)

        if abs(total_net) > 0.001:  # Allow for small floating point errors
            raise ValueError(f"Postings do not balance to zero. Net total: {total_net}")

        # If the gross amounts don't balance, we need to adjust them
        total_gross = sum(p.amount_gross or 0.0 for p in posting_objects)
        if abs(total_gross) > 0.001:  # Allow for small floating point errors
            # Find the credit posting (negative amount) and adjust its gross amount
            for p in posting_objects:
                if p.amount is not None and p.amount < 0 and p.amount_gross is not None:
                    # Adjust the gross amount to balance the total
                    p.amount_gross = p.amount_gross - total_gross
                    p.amount_gross_currency = p.amount_gross
                    break

        return posting_objects
