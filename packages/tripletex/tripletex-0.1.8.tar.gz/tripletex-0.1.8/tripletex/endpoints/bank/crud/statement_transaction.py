from typing import Any, ClassVar, Dict, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import BankTransaction, BankTransactionResponse


class TripletexBankStatementTransactions(TripletexCrud[BankTransaction]):
    """API endpoint for accessing bank statement transactions in Tripletex."""

    _resource_path: ClassVar[str] = "transaction"
    _datamodel: ClassVar[Type[BankTransaction]] = BankTransaction
    _api_response_model: ClassVar[Type[BankTransactionResponse]] = BankTransactionResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def list_by_statement(
        self,
        statement_id: int,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[BankTransaction]:
        """
        Find bank transactions for a specific bank statement.

        Args:
            statement_id: ID of the bank statement
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of BankTransaction objects.
        """
        params: JSONDict = {
            "bankStatementId": statement_id,
            "from": from_index,
            "count": count,
        }

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use the base list method from TripletexCrud
        response_obj = self.list(params=params)

        # Return the values list
        return response_obj.values

    def get_details(
        self,
        transaction_id: int,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get additional details about a transaction by ID.

        Args:
            transaction_id: ID of the bank transaction
            fields: Fields filter pattern

        Returns:
            Dictionary containing additional details about the transaction.
        """
        params: JSONDict = {}
        if fields:
            params["fields"] = fields

        # Use custom_action for the details endpoint
        response = self.custom_action(
            action="details",
            method="get",
            resource_id=str(transaction_id),
            params=params,
        )

        # Convert the response to a dictionary
        if hasattr(response, "model_dump"):
            # If it's a Pydantic model, convert it to a dict
            return response.model_dump()
        elif isinstance(response, dict):
            if "value" in response:
                # If it's a dict with a 'value' key, return the value
                if isinstance(response["value"], dict):
                    return response["value"]
                elif hasattr(response["value"], "model_dump"):
                    return response["value"].model_dump()
            # Otherwise return the dict as is
            return response
        else:
            # If it's something else, convert it to a dict if possible
            return {"data": str(response)}
