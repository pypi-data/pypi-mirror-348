from typing import TYPE_CHECKING, ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import (
    BankReconciliation,
    BankReconciliationAdjustment,
    BankReconciliationCreate,
    BankReconciliationResponse,
    BankReconciliationUpdate,
    UnmatchedTransactionsCsv,
)

if TYPE_CHECKING:
    from tripletex.endpoints.bank.crud.internal_match import TripletexBankReconciliationInternalMatch


class TripletexBankReconciliation(TripletexCrud[BankReconciliation]):
    """API endpoint for accessing bank reconciliation in Tripletex."""

    _resource_path: ClassVar[str] = "reconciliation"
    _datamodel: ClassVar[Type[BankReconciliation]] = BankReconciliation
    _create_model: ClassVar[Type[BankReconciliationCreate]] = BankReconciliationCreate
    _update_model: ClassVar[Type[BankReconciliationUpdate]] = BankReconciliationUpdate
    _api_response_model: ClassVar[Type[BankReconciliationResponse]] = BankReconciliationResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update", "destroy"]
    internal_match: "TripletexBankReconciliationInternalMatch"

    def get_last(
        self,
        account_id: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> BankReconciliationResponse:
        """
        Get the last bank reconciliation.

        Args:
            account_id: ID of the account
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            BankReconciliationResponse object containing the last bank reconciliation.
        """
        params: JSONDict = {
            "from": from_index,
            "count": count,
        }

        if account_id is not None:
            params["accountId"] = account_id
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use custom_action for the >last endpoint
        response_obj = self.custom_action(
            action=">last",
            method="get",
            params=params,
        )

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._api_response_model):
            raise TypeError(f"Expected {self._api_response_model.__name__}, got {type(response_obj)}")

        # Handle the case where value is None
        if hasattr(response_obj, "value") and response_obj.value is None:
            response_obj.value = None  # Explicitly set to None to avoid instantiation with None

        return response_obj

    def get_last_closed(
        self,
        account_id: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> BankReconciliationResponse:
        """
        Get the last closed bank reconciliation.

        Args:
            account_id: ID of the account
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            BankReconciliationResponse object containing the last closed bank reconciliation.
        """
        params: JSONDict = {
            "from": from_index,
            "count": count,
        }

        if account_id is not None:
            params["accountId"] = account_id
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use custom_action for the >lastClosed endpoint
        response_obj = self.custom_action(
            action=">lastClosed",
            method="get",
            params=params,
        )

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._api_response_model):
            raise TypeError(f"Expected {self._api_response_model.__name__}, got {type(response_obj)}")

        # Handle the case where value is None
        if hasattr(response_obj, "value") and response_obj.value is None:
            response_obj.value = None  # Explicitly set to None to avoid instantiation with None

        return response_obj

    def get_closed_with_unmatched_transactions(
        self,
        account_id: int,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> BankReconciliationResponse:
        """
        Get closed bank reconciliations with unmatched transactions.

        Args:
            account_id: ID of the account (required)
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            BankReconciliationResponse object containing closed bank reconciliations with unmatched transactions.
        """
        params: JSONDict = {
            "from": from_index,
            "count": count,
            "accountId": account_id,
        }

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use custom_action for the closedWithUnmatchedTransactions endpoint
        response_obj = self.custom_action(
            action="closedWithUnmatchedTransactions",
            method="get",
            params=params,
        )

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._api_response_model):
            raise TypeError(f"Expected {self._api_response_model.__name__}, got {type(response_obj)}")

        # Handle the case where value is None
        if hasattr(response_obj, "value") and response_obj.value is None:
            response_obj.value = None  # Explicitly set to None to avoid instantiation with None

        return response_obj

    def apply_adjustment(
        self,
        resource_id: str,
        adjustment_amount: float,
        description: Optional[str] = None,
    ) -> BankReconciliation:
        """
        Apply an adjustment to a bank reconciliation.

        Args:
            resource_id: ID of the bank reconciliation
            adjustment_amount: Amount to adjust
            description: Optional description for the adjustment

        Returns:
            BankReconciliation object with the applied adjustment.
        """
        data = BankReconciliationAdjustment(
            adjustment_amount=adjustment_amount,
            description=description,
        )

        # Use custom_action for the /:adjustment endpoint
        response_obj = self.custom_action(
            action=f"{resource_id}/:adjustment",
            method="put",
            data=data,
        )

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._datamodel):
            raise TypeError(f"Expected {self._datamodel.__name__}, got {type(response_obj)}")

        return response_obj

    def export_unmatched_transactions_csv(
        self,
        file_format: str = "CSV",
    ) -> bytes:
        """
        Export unmatched transactions as CSV.

        Args:
            file_format: Format of the export (default: CSV)

        Returns:
            Bytes containing the CSV data.
        """
        data = UnmatchedTransactionsCsv(file_format=file_format)

        # Use custom_action for the transactions/unmatched:csv endpoint
        response = self.custom_action(
            action="transactions/unmatched:csv",
            method="put",
            data=data,
            raw_response=True,
        )

        # Return the raw bytes
        return response.content
