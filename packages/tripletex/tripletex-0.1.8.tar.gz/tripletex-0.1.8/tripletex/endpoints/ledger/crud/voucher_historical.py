from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    VoucherHistorical,
    VoucherHistoricalResponse,
)

from .voucher import TripletexVoucher


class TripletexVoucherHistorical(TripletexCrud[VoucherHistorical]):
    """API methods for interacting with historical ledger vouchers."""

    _resource_path: ClassVar[str] = "historical"
    _datamodel: ClassVar[Type[VoucherHistorical]] = VoucherHistorical
    _api_response_model: ClassVar[Type[VoucherHistoricalResponse]] = VoucherHistoricalResponse
    _parent_resource: ClassVar[Type[TripletexVoucher]] = TripletexVoucher

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None) -> VoucherHistoricalResponse:
        """
        List historical vouchers.

        Args:
            parent_id: Optional parent ID if this is a nested resource
            params: Optional query parameters. Must include 'dateFrom' and 'dateTo'.

        Returns:
            VoucherHistoricalResponse containing a list of VoucherHistorical objects

        Raises:
            UnprocessableEntityError: If dateFrom or dateTo is missing
        """
        if params is None:
            params = {}

        # Ensure required parameters are present
        if "dateFrom" not in params or "dateTo" not in params:
            # Default to current date if not provided
            from datetime import datetime, timedelta

            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            if "dateFrom" not in params:
                params["dateFrom"] = yesterday
            if "dateTo" not in params:
                params["dateTo"] = today

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
    ) -> VoucherHistoricalResponse:
        """
        Find historical vouchers corresponding with sent data.

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
            VoucherHistoricalResponse containing a list of VoucherHistorical objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if number:
            params["number"] = number
        if number_from:
            params["numberFrom"] = number_from
        if number_to:
            params["numberTo"] = number_to

        # Handle date parameters - required by the API
        from datetime import datetime, timedelta

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        params["dateFrom"] = date_from if date_from else yesterday
        params["dateTo"] = date_to if date_to else today

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def upload_attachment(self, voucher_id: int, file_path: str) -> VoucherHistorical:
        """
        Upload an attachment to a historical voucher.

        Args:
            voucher_id: The ID of the historical voucher to attach the file to.
            file_path: Path to the file to upload.

        Returns:
            VoucherHistorical: The updated historical voucher object with the attachment.

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
        # Parse as VoucherHistorical (wrapped in "value")
        return self._datamodel.model_validate(data["value"])

    def create_historical(self, data: JSONDict) -> VoucherHistorical:
        """
        Create a historical voucher.
        POST /ledger/voucher/historical

        Args:
            data: The data for creating the historical voucher.

        Returns:
            VoucherHistorical: The created historical voucher.
        """
        # Use the base endpoint directly, not /historical/historical
        endpoint = self._get_endpoint()
        raw_response = self.client.post(endpoint, data=data)
        return self._datamodel.model_validate(raw_response["value"])

    def create_employee(self, data: JSONDict) -> VoucherHistorical:
        """
        Create an employee historical voucher.
        POST /ledger/voucher/historical/employee

        Args:
            data: The data for creating the employee historical voucher.

        Returns:
            VoucherHistorical: The created employee historical voucher.
        """
        endpoint = self._get_endpoint("employee")
        raw_response = self.client.post(endpoint, data=data)
        return self._datamodel.model_validate(raw_response["value"])

    def close_postings(self, data: Optional[JSONDict] = None) -> List[VoucherHistorical]:
        """
        Close postings for historical vouchers.
        PUT /ledger/voucher/historical/:closePostings

        Args:
            data: Optional data for closing postings.

        Returns:
            List[VoucherHistorical]: List of affected historical vouchers.
        """
        endpoint = self._get_endpoint(":closePostings")
        raw_response = self.client.put(endpoint, data=data or {})
        return [self._datamodel.model_validate(item) for item in raw_response["values"]]

    def reverse_historical_vouchers(self, data: JSONDict) -> List[VoucherHistorical]:
        """
        Reverse historical vouchers.
        PUT /ledger/voucher/historical/:reverseHistoricalVouchers

        Args:
            data: Data for reversing historical vouchers, including voucher IDs and date.

        Returns:
            List[VoucherHistorical]: List of reversed historical vouchers.
        """
        endpoint = self._get_endpoint(":reverseHistoricalVouchers")
        raw_response = self.client.put(endpoint, data=data)
        return [self._datamodel.model_validate(item) for item in raw_response["values"]]
