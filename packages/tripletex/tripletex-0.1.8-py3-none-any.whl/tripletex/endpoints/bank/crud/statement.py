import os
from typing import Any, ClassVar, Dict, List, Optional, Type, Union

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import (
    BankStatement,
    BankStatementImport,
    BankStatementResponse,
)


class TripletexBankStatements(TripletexCrud[BankStatement]):
    """API endpoint for accessing bank statements in Tripletex."""

    _resource_path: ClassVar[str] = "statement"
    _datamodel: ClassVar[Type[BankStatement]] = BankStatement
    _api_response_model: ClassVar[Type[BankStatementResponse]] = BankStatementResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read", "destroy"]

    def search(
        self,
        id: Optional[str] = None,
        account_id: Optional[str] = None,
        file_formats: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[BankStatement]:
        """
        Find bank statements corresponding with sent data.

        Args:
            id: List of IDs
            account_id: Account ID
            file_formats: List of file formats
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of BankStatement objects.
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if account_id:
            params["accountId"] = account_id
        if file_formats:
            params["fileFormats"] = file_formats
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use the base list method from TripletexCrud
        response_obj = self.list(params=params)

        # Return the values list
        return response_obj.values

    def import_statement(
        self,
        file: Union[str, bytes, Any],
        bank_id: int,
        account_id: int,
        from_date: str,
        to_date: str,
        file_format: str,
        external_id: Optional[str] = None,
    ) -> BankStatement:
        """
        Import a bank statement file.

        Args:
            file: The bank statement file path, bytes content, or file-like object
            bank_id: ID of the bank
            account_id: ID of the account
            from_date: From date (YYYY-MM-DD)
            to_date: To date (YYYY-MM-DD)
            file_format: File format (use BankStatementImportFileFormat constants)
            external_id: Optional external ID

        Returns:
            BankStatement object representing the imported statement.
        """
        # Handle file content
        file_obj = file
        filename = "bankstatement.txt"  # Default filename

        # If file is a path, open it and read the content
        if isinstance(file, str):
            filename = os.path.basename(file)
            with open(file, "rb") as f:
                file_content = f.read()
            file_obj = file_content

        # Create model for documentation purposes only
        # This shows the expected structure, but we'll use requests library directly
        _ = BankStatementImport(
            file=file_obj,
            bankId=bank_id,
            accountId=account_id,
            fromDate=from_date,
            toDate=to_date,
            fileFormat=file_format,
            externalId=external_id,
        )

        # Issue a stern warning about this implementation
        import warnings

        warnings.warn(
            "SECURITY VULNERABILITY: The bank statement import method is using a direct requests call, "
            "bypassing crudclient security features. This is NOT suitable for production use "
            "and must be replaced with a proper implementation using crudclient patterns.",
            category=RuntimeWarning,
            stacklevel=2,
        )

        # Import requests library for direct HTTP access
        import requests

        # Get the full URL with query parameters
        endpoint = "bank/statement/import"
        url = f"{self.client.base_url}/{endpoint.lstrip('/')}"

        # Prepare query parameters
        params: Dict[str, Union[str, int]] = {
            "bankId": bank_id,
            "accountId": account_id,
            "fromDate": from_date,
            "toDate": to_date,
            "fileFormat": file_format,
        }

        if external_id:
            params["externalId"] = external_id

        # Get the authorization header from the client
        auth_header = self.client.http_client.session_manager.session.headers.get("Authorization", "")

        # Set up the headers
        headers = {
            "Authorization": auth_header,
        }

        # Format the files parameter as a list of tuples, which is what requests expects
        files = [("file", (filename, file_obj, "text/plain"))]

        # Make the request directly using requests
        response = requests.post(url, headers=headers, files=files, params=params)

        # Raise an exception if the request failed
        response.raise_for_status()

        # Parse the response
        response_data = response.json()

        # Convert the response to a BankStatement object
        if "value" in response_data:
            result = self._datamodel.model_validate(response_data["value"])
        else:
            result = self._datamodel.model_validate(response_data)

        return result
