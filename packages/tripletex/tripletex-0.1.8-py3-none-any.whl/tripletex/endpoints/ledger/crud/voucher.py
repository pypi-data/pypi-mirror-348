import logging  # Add logging import
from typing import ClassVar, List, Optional, Tuple, Type, Union

import requests
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models.gbat10 import VoucherImportGbat10

# Import base models used by the class definition directly from voucher.py
from tripletex.endpoints.ledger.models.voucher import (
    Voucher,
    VoucherCreate,
    VoucherResponse,
    VoucherUpdate,
)
from tripletex.utils import ensure_date_params

from .ledger import TripletexLedger

logger = logging.getLogger(__name__)  # Initialize logger


class TripletexVoucher(TripletexCrud[Voucher]):
    """API methods for interacting with ledger vouchers."""

    _resource_path: ClassVar[str] = "voucher"
    _datamodel: ClassVar[Type[Voucher]] = Voucher
    _create_model: ClassVar[Type[VoucherCreate]] = VoucherCreate
    _update_model: ClassVar[Type[VoucherUpdate]] = VoucherUpdate
    _api_response_model: ClassVar[Type[VoucherResponse]] = VoucherResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update", "destroy"]

    def create(self, data: Union[JSONDict, VoucherCreate], parent_id: Optional[str] = None, send_to_ledger: bool = True) -> Voucher:
        """
        Create a new voucher.

        Args:
            data: The voucher data to create
            parent_id: Optional parent ID if this is a nested resource
            send_to_ledger: Whether to send the voucher to ledger. Defaults to True.

        Returns:
            The created voucher
        """
        # Extract sendToLedger parameter and pass it as a query parameter
        params = {"sendToLedger": send_to_ledger}

        # Call the parent create method with the query parameter
        return super().create(data=data, parent_id=parent_id, params=params)

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None):
        """
        List vouchers.

        Args:
            parent_id: Optional parent ID if this is a nested resource
            params: Optional query parameters. Must include 'dateFrom' and 'dateTo'.

        Returns:
            VoucherResponse object containing a list of Voucher objects

        Raises:
            UnprocessableEntityError: If dateFrom or dateTo is missing
        """

        # Ensure required date parameters are present, defaulting if necessary
        params = ensure_date_params(params)

        return super().list(parent_id=parent_id, params=params)

    def search(
        self,
        number: Optional[str] = None,
        number_from: Optional[int] = None,
        number_to: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> VoucherResponse:
        """
        Find vouchers corresponding with sent data.

        Args:
            number: Voucher number
            number_from: From voucher number
            number_to: To voucher number
            date_from: From and including date (format YYYY-MM-DD). Required.
            date_to: To and including date (format YYYY-MM-DD). Required.
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            VoucherResponse containing a list of Voucher objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if number:
            params["number"] = number
        if number_from:
            params["numberFrom"] = number_from
        if number_to:
            params["numberTo"] = number_to

        # Handle date parameters - required by the API
        # If date_from or date_to are provided, use them; otherwise, use defaults
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        params = ensure_date_params(params)

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return super().list(params=params)

    def get_options(self, voucher_id: str) -> JSONDict:
        """
        Get meta information about operations available for this voucher (e.g., if deletable).
        GET /ledger/voucher/{id}/options
        Returns a dict, not a Voucher model.
        """
        # Bypass model conversion for this subresource
        endpoint = self._get_endpoint(str(voucher_id), "options")
        return self.client.get(endpoint)

    def get_pdf(self, voucher_id: str) -> requests.Response:
        """
        Get PDF representation of voucher by ID.
        GET /ledger/voucher/{voucherId}/pdf

        Returns the raw HTTP response object for full header/content access.
        """
        endpoint = self._get_endpoint(str(voucher_id), "pdf")
        response = self.client.http_client.request_raw("GET", endpoint)
        return response

    def list_non_posted(self, params: Optional[JSONDict] = None) -> VoucherResponse:
        """
        Find non-posted vouchers.
        GET /ledger/voucher/>nonPosted
        Returns a list of non-posted vouchers.
        """
        # The >nonPosted endpoint returns a response that already has the structure we need
        # We just need to use the client directly to get the raw response
        endpoint = self._get_endpoint(">nonPosted")
        raw_response = self.client.get(endpoint, params=params)
        return self._api_response_model.model_validate(raw_response)

    def download_pdf(self, voucher_id: str, file_path: Optional[str] = None) -> Tuple[str, str]:
        """
        Download PDF for voucher by ID and save to file_path.
        Returns the file path and filename.
        """
        import re

        response = self.get_pdf(voucher_id)
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = "voucher.pdf"
        match = re.search(r'filename="?([^";]+)"?', content_disposition)
        if match:
            filename = match.group(1)
        pdf_bytes = response.content
        if file_path is None:
            file_path = filename
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return file_path, filename

    def upload_attachment(self, voucher_id: int, file_path: str) -> Voucher:
        """
        Upload an attachment to a voucher.

        Args:
            voucher_id: The ID of the voucher to attach the file to.
            file_path: Path to the file to upload.

        Returns:
            Voucher: The updated voucher object with the attachment.

        Raises:
            ValueError: If the file is not a PDF. The Tripletex API only supports
                       PDF files for voucher attachments. This is an intentional
                       limitation of the API, not a restriction imposed by this client.
        """
        import os

        endpoint = self._get_endpoint(str(voucher_id), "attachment")
        url = self.client.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            # IMPORTANT: The Tripletex API only accepts PDF files for voucher attachments.
            # This is an API limitation, not a client restriction.
            if not filename.lower().endswith(".pdf"):
                raise ValueError("Only PDF files are allowed for voucher attachments. This is a limitation of the Tripletex API.")
            files = {"file": (filename, f, "application/pdf")}
            # Use the requests session directly for multipart upload
            response = self.client.session.post(url, files=files)
            response.raise_for_status()
            data = response.json()
        # Parse as Voucher (wrapped in "value")
        return self._datamodel.model_validate(data["value"])

    def destroy(self, resource_id: str, parent_id: Optional[str] = None) -> None:
        """
        Delete voucher by ID.
        DELETE /ledger/voucher/{id}

        Args:
            resource_id: The ID of the voucher to delete
            parent_id: Optional parent ID if this is a nested resource

        Returns:
            None
        """
        return super().destroy(resource_id=resource_id, parent_id=parent_id)

    # Alias destroy to delete for compatibility with existing tests
    delete = destroy

    def destroy_attachment(
        self, voucher_id: str, attachment_id: str, version: Optional[int] = None, send_to_inbox: bool = False, split: bool = False
    ) -> None:
        """
        Delete an attachment from a voucher.
        DELETE /ledger/voucher/{voucherId}/attachment

        Args:
            voucher_id: The ID of the voucher
            attachment_id: The ID of the attachment to delete (used in query params)
            version: Optional version number
            send_to_inbox: Whether to send to inbox. Default: False
            split: Whether to split. Default: False

        Returns:
            None
        """
        # Construct the endpoint path - attachment ID is not part of the path
        endpoint = self._get_endpoint(str(voucher_id), "attachment")

        # Prepare optional parameters
        params = {"id": attachment_id}  # Attachment ID is passed as a query parameter
        if version is not None:
            params["version"] = str(version)
        if send_to_inbox:
            params["sendToInbox"] = str(send_to_inbox).lower()
        if split:
            params["split"] = str(split).lower()

        # Use the client's delete method directly
        self.client.delete(endpoint, params=params)

    # Alias delete_attachment to destroy_attachment for backward compatibility
    delete_attachment = destroy_attachment

    def voucher_reception(self, params: Optional[JSONDict] = None) -> VoucherResponse:
        """
        Get voucher reception list.
        GET /ledger/voucher/>voucherReception

        This endpoint returns vouchers that are in the reception phase.

        Args:
            params: Optional query parameters for filtering, pagination, etc.

        Returns:
            VoucherResponse containing a list of Voucher objects
        """
        # Use the _get_endpoint method with ">voucherReception" to construct the correct URL
        endpoint = self._get_endpoint(">voucherReception")
        raw_response = self.client.get(endpoint, params=params)

        # Convert the response to a VoucherResponse object
        return self._api_response_model.model_validate(raw_response)

    def external_voucher_number(
        self,
        external_voucher_number: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> VoucherResponse:
        """
        Find vouchers based on the external voucher number.
        GET /ledger/voucher/>externalVoucherNumber

        Args:
            external_voucher_number: The external voucher number to search for
            from_index: From index (for pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            VoucherResponse containing a list of Voucher objects matching the external voucher number
        """
        # Prepare query parameters
        params: JSONDict = {"from": from_index, "count": count}

        if external_voucher_number:
            params["externalVoucherNumber"] = external_voucher_number
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use the _get_endpoint method with ">externalVoucherNumber" to construct the correct URL
        # This is similar to how voucher_reception is implemented
        endpoint = self._get_endpoint(">externalVoucherNumber")
        raw_response = self.client.get(endpoint, params=params)

        # Convert the response to a VoucherResponse object
        return self._api_response_model.model_validate(raw_response)

    def import_gbat10(self, data: Union[JSONDict, "VoucherImportGbat10"]) -> None:
        """
        Import GBAT10 format vouchers.
        POST /ledger/voucher/importGbat10

        This endpoint allows uploading a file in GBAT10 format to create vouchers.
        The file is sent as a multipart form along with parameters.

        Args:
            data: VoucherImportGbat10 object or dict containing:
                - generate_vat_postings: If the import should generate VAT postings
                - file_path: Path to the file to upload
                - encoding: The file encoding (defaults to 'utf-8')
                - content: Optional content to validate or write to file_path

        Returns:
            None: The API doesn't return any data on success

        Raises:
            ValueError: If the file doesn't exist or can't be read, or if the GBAT10 content is invalid
            HTTPError: If the API request fails
        """
        import os

        from tripletex.endpoints.ledger.models.gbat10 import VoucherImportGbat10

        # Convert dict to model if needed
        if isinstance(data, dict):
            data = VoucherImportGbat10.model_validate(data)

        # Check if file exists
        if not os.path.exists(data.file_path):
            # If content is provided, write it to the file
            if data.content:
                data.write_content_to_file()
            else:
                # If no content and auto-generation is not disabled, generate a sample file
                # Otherwise, raise an error
                try:
                    data.content = None  # Ensure content is None to trigger sample generation
                    data.write_content_to_file()
                except ValueError:
                    # If write_content_to_file raises a ValueError, it means auto-generation
                    # is disabled (e.g., in tests). In this case, we should raise a "File not found" error.
                    raise ValueError(f"File not found: {data.file_path}")

        # Validate file exists after potential creation
        if not os.path.exists(data.file_path):
            raise ValueError(f"File not found: {data.file_path}")

        # Validate the GBAT10 content
        try:
            data.validate_content()
        except ValueError as validation_error:
            # If validation fails, the file might exist but have invalid content
            # We'll raise a more specific error
            raise ValueError(f"Invalid GBAT10 file: {validation_error}")

        # Prepare the endpoint
        endpoint = self._get_endpoint("importGbat10")
        url = self.client.base_url.rstrip("/") + "/" + endpoint.lstrip("/")

        # Open the file and prepare the multipart form data
        with open(data.file_path, "rb") as f:
            filename = os.path.basename(data.file_path)
            files = {"file": (filename, f)}
            form_data = {"generateVatPostings": str(data.generate_vat_postings).lower(), "encoding": data.encoding}

            # Use the requests session directly for multipart upload
            response = self.client.session.post(url, files=files, data=form_data)
            response.raise_for_status()

        # The endpoint doesn't return any data on success
        return None

    def update(
        self,
        resource_id: str,
        data: Union[JSONDict, VoucherUpdate],
        parent_id: Optional[str] = None,
        send_to_ledger: bool = False,
    ) -> Voucher:
        """
        Update a voucher by ID.
        PUT /ledger/voucher/{id}

        Args:
            resource_id: The ID of the voucher to update
            data: The updated voucher data (VoucherUpdate model or dict)
            parent_id: Optional parent ID if this is a nested resource
            send_to_ledger: Whether to send the voucher to ledger after update.
                              Defaults to False. If True and voucher is not yet in ledger,
                              it will be sent.

        Returns:
            The updated voucher
        """
        # First, update the voucher without any special sendToLedger query param
        updated_voucher = super().update(resource_id=resource_id, data=data, parent_id=parent_id)

        # Check if we need to send it to ledger
        # A voucher is in the ledger if it has a final 'number' (not just a 'tempNumber')
        # The 'number' field is populated when it's sent to ledger.
        is_in_ledger = updated_voucher.number is not None

        if send_to_ledger and not is_in_ledger:
            if updated_voucher.id is None:
                # This should not happen if super().update() was successful
                raise ValueError("Cannot send voucher to ledger: updated voucher has no ID.")
            logger.info(f"Voucher {updated_voucher.id} updated and not in ledger. Sending to ledger as requested.")
            return self.send_to_ledger(voucher_id=str(updated_voucher.id))
        elif is_in_ledger:
            logger.info(
                f"Voucher {updated_voucher.id} is already in ledger (number: {updated_voucher.number}). No action needed for send_to_ledger={send_to_ledger}."
            )
        else:  # not send_to_ledger and not is_in_ledger
            logger.info(f"Voucher {updated_voucher.id} updated. send_to_ledger is False and voucher is not in ledger. No further action.")

        return updated_voucher

    def reverse_voucher(self, voucher_id: str, date: Optional[str] = None) -> Voucher:
        """
        Reverse a voucher.
        PUT /ledger/voucher/{id}/reverse

        Creates a copy of the voucher with opposite sign amounts and links them together.

        Args:
            voucher_id: The ID of the voucher to reverse
            date: Optional date for the reversed voucher. If not provided, the current date is used.

        Returns:
            The newly created reversed voucher
        """
        data = {}
        if date:
            data["date"] = date

        # Use custom_action with the :reverse action and PUT method
        endpoint = self._get_endpoint(str(voucher_id), ":reverse")
        raw_response = self.client.put(endpoint, data=data)

        # Convert the response to a Voucher object (from the "value" field)
        return self._datamodel.model_validate(raw_response["value"])

    def update_list(self, vouchers: List[Union[JSONDict, VoucherUpdate]]) -> List[Voucher]:
        """
        Update multiple vouchers.
        PUT /ledger/voucher/list

        Args:
            vouchers: List of voucher data to update (VoucherUpdate models or dicts)

        Returns:
            List of updated vouchers
        """
        # Prepare the data - convert models to dicts if needed
        data_list = []
        for voucher in vouchers:
            if hasattr(voucher, "model_dump"):
                data_list.append(voucher.model_dump(mode="json", by_alias=True))
            else:
                data_list.append(voucher)

        # Wrap the list in a dictionary with a "values" key
        data = {"values": data_list}

        # Use custom_action with the "list" action and PUT method
        endpoint = self._get_endpoint("list")
        raw_response = self.client.put(endpoint, data=data)

        # Convert the response to a list of Voucher objects
        return [self._datamodel.model_validate(item) for item in raw_response["values"]]

    def send_to_ledger(self, voucher_id: str) -> Voucher:
        """
        Send a voucher to ledger.
        PUT /ledger/voucher/{id}/sendToLedger

        Args:
            voucher_id: The ID of the voucher to send to ledger

        Returns:
            The updated voucher
        """
        # Use custom_action with the :sendToLedger action and PUT method
        endpoint = self._get_endpoint(str(voucher_id), ":sendToLedger")
        raw_response = self.client.put(endpoint)

        # Convert the response to a Voucher object
        return self._datamodel.model_validate(raw_response["value"])

    def send_to_inbox(self, voucher_id: str) -> Voucher:
        """
        Send a voucher to inbox.
        PUT /ledger/voucher/{id}/sendToInbox

        Args:
            voucher_id: The ID of the voucher to send to inbox

        Returns:
            The updated voucher
        """
        # Use custom_action with the :sendToInbox action and PUT method
        endpoint = self._get_endpoint(str(voucher_id), ":sendToInbox")
        raw_response = self.client.put(endpoint)

        # Convert the response to a Voucher object
        return self._datamodel.model_validate(raw_response["value"])

    def import_document(
        self,
        file_path: str,
        description: Optional[str] = None,
        voucher_date: Optional[str] = None,
        voucher_type_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        project_id: Optional[int] = None,
        send_to_ledger: bool = True,
        split_by_vat: bool = False,
    ) -> Voucher:
        """
        Import a document as a voucher.
        POST /ledger/voucher/importDocument

        This endpoint allows uploading a document file to create a voucher.
        The file is sent as a multipart form along with parameters.

        Args:
            file_path: Path to the file to upload
            description: Optional description for the voucher
            voucher_date: Optional date for the voucher (format YYYY-MM-DD)
            voucher_type_id: Optional voucher type ID
            supplier_id: Optional supplier ID
            employee_id: Optional employee ID
            department_id: Optional department ID
            project_id: Optional project ID
            send_to_ledger: Whether to send the voucher to ledger (default: True)
            split_by_vat: Whether to split the voucher by VAT (default: False)

        Returns:
            The created voucher

        Raises:
            ValueError: If the file doesn't exist or can't be read
            HTTPError: If the API request fails
        """
        import mimetypes
        import os

        # Check if file exists
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        # Prepare the endpoint
        endpoint = self._get_endpoint("importDocument")
        url = self.client.base_url.rstrip("/") + "/" + endpoint.lstrip("/")

        # Determine the file's MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            # Default to application/octet-stream if type can't be determined
            mime_type = "application/octet-stream"

        # Prepare form data
        form_data = {}
        if description:
            form_data["description"] = description
        if voucher_date:
            form_data["voucherDate"] = voucher_date
        if voucher_type_id:
            form_data["voucherTypeId"] = str(voucher_type_id)
        if supplier_id:
            form_data["supplierId"] = str(supplier_id)
        if employee_id:
            form_data["employeeId"] = str(employee_id)
        if department_id:
            form_data["departmentId"] = str(department_id)
        if project_id:
            form_data["projectId"] = str(project_id)

        form_data["sendToLedger"] = str(send_to_ledger).lower()
        form_data["splitByVat"] = str(split_by_vat).lower()

        # Open the file and prepare the multipart form data
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            files = {"file": (filename, f, mime_type)}

            # Use the requests session directly for multipart upload
            response = self.client.session.post(url, files=files, data=form_data)
            response.raise_for_status()
            data = response.json()

        # Parse as Voucher - may be directly in the response or in a "value" key
        if "value" in data:
            return self._datamodel.model_validate(data["value"])
        else:
            return self._datamodel.model_validate(data)
