from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import Bank, BankResponse


class TripletexBanks(TripletexCrud[Bank]):
    """API endpoint for accessing bank information in Tripletex."""

    _resource_path: ClassVar[str] = "bank"
    _datamodel: ClassVar[Type[Bank]] = Bank
    _api_response_model: ClassVar[Type[BankResponse]] = BankResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        id: Optional[str] = None,
        register_numbers: Optional[str] = None,
        is_bank_reconciliation_support: Optional[bool] = None,
        is_auto_pay_supported: Optional[bool] = None,
        is_ztl_supported: Optional[bool] = None,
        query: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> BankResponse:
        """
        Find banks corresponding with sent data.

        Args:
            id: List of IDs
            register_numbers: List of register numbers
            is_bank_reconciliation_support: Filter by bank reconciliation support
            is_auto_pay_supported: Filter by auto pay support
            is_ztl_supported: Filter by ZTL support
            query: Text search in name field
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            BankResponse object containing a list of Bank objects.
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if register_numbers:
            params["registerNumbers"] = register_numbers
        if is_bank_reconciliation_support is not None:
            params["isBankReconciliationSupport"] = is_bank_reconciliation_support
        if is_auto_pay_supported is not None:
            params["isAutoPaySupported"] = is_auto_pay_supported
        if is_ztl_supported is not None:
            params["isZtlSupported"] = is_ztl_supported
        if query:
            params["query"] = query
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use the base list method from TripletexCrud
        response_obj = self.list(params=params)

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._api_response_model):
            raise TypeError(f"Expected {self._api_response_model.__name__} from list, got {type(response_obj)}")

        return response_obj
