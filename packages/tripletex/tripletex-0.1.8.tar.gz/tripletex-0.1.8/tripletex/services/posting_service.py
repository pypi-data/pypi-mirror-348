"""Service for creating posting drafts from simple information."""

from typing import Optional

from crudclient.exceptions import NotFoundError

from tripletex.core.api import TripletexAPI
from tripletex.core.models import IdRef
from tripletex.endpoints.ledger.models.posting import PostingCreate
from tripletex.endpoints.supplier.models import Supplier


class PostingService:
    """Service for creating posting drafts from simple information."""

    def __init__(self, api_client: TripletexAPI):
        """Initialize the service with a Tripletex API client.

        Args:
            api_client: The Tripletex API client to use for API calls.
        """
        self.api_client = api_client

    def create_posting_draft(
        self,
        description: str,
        account_no: str,
        amount: float,
        supplier_name: Optional[str] = None,
        supplier_org_nr: Optional[str] = None,
        row: int = 1,
    ) -> PostingCreate:
        """Create a posting draft from simple information.

        Args:
            description: Description of the posting.
            account_no: Account number to use for the posting.
            amount: Amount for the posting.
            supplier_name: Optional name of the supplier.
            supplier_org_nr: Optional organization number of the supplier.
            row: Row number within the voucher (default: 1).

        Returns:
            A PostingCreate model instance ready to be used in a voucher.

        Raises:
            NotFoundError: If the account or supplier cannot be found.
        """
        # Find the account by number
        account = self.api_client.ledger.account.get_by_number_or_404(account_no)

        # Create the posting draft
        posting_draft = PostingCreate(
            description=description,
            account=IdRef(id=account.id),
            amount=amount,
            row=row,
        )

        # Set the VAT type if available from the account
        if account.vat_type and account.vat_type.id:
            posting_draft.vat_type = IdRef(id=account.vat_type.id)

        # Find the supplier if name or organization number is provided
        if supplier_name or supplier_org_nr:
            supplier = self._find_supplier(supplier_name, supplier_org_nr)
            if supplier:
                posting_draft.supplier = IdRef(id=supplier.id)

        return posting_draft

    def _find_supplier(self, supplier_name: Optional[str], supplier_org_nr: Optional[str]) -> Optional[Supplier]:
        """Find a supplier by name and/or organization number.

        Args:
            supplier_name: Name of the supplier to find.
            supplier_org_nr: Organization number of the supplier to find.

        Returns:
            The supplier if found, None otherwise.
        """
        if not supplier_name and not supplier_org_nr:
            return None

        try:
            # Try to find by organization number first (more specific)
            if supplier_org_nr:
                return self.api_client.suppliers.get_by_organization_number_or_404(supplier_org_nr)

            # Then try by name
            if supplier_name:
                return self.api_client.suppliers.get_by_name_or_404(supplier_name)

        except NotFoundError:
            # If not found with the exact methods, try a more flexible search
            if supplier_name:
                # Search with name as a parameter and get the first match
                response = self.api_client.suppliers.search(name=supplier_name, count=1)
                # The response is a SupplierResponse object with a values attribute
                suppliers = response.values if hasattr(response, "values") else []
                if suppliers:
                    return suppliers[0]

        # If we get here, no supplier was found
        return None
