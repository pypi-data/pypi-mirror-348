from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models.accounting_period import (
    AccountingPeriod,
    AccountingPeriodResponse,
)

from .ledger import TripletexLedger


class TripletexAccountingPeriod(TripletexCrud[AccountingPeriod]):
    """API methods for interacting with ledger accounting periods."""

    _resource_path: ClassVar[str] = "accountingPeriod"
    _datamodel: ClassVar[Type[AccountingPeriod]] = AccountingPeriod
    _api_response_model: ClassVar[Type[AccountingPeriodResponse]] = AccountingPeriodResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        id: Optional[str] = None,
        number_from: Optional[int] = None,
        number_to: Optional[int] = None,
        start_from: Optional[str] = None,
        start_to: Optional[str] = None,
        end_from: Optional[str] = None,
        end_to: Optional[str] = None,
        from_index: int = 0,
        count: int = 1400,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> AccountingPeriodResponse:
        """
        Find accounting periods corresponding with sent data.

        Args:
            id: List of IDs
            number_from: From and including
            number_to: To and excluding
            start_from: From and including
            start_to: To and excluding
            end_from: From and including
            end_to: To and excluding
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            AccountingPeriodResponse containing a list of AccountingPeriod objects
        """

        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = int(id)
        if number_from:
            params["numberFrom"] = number_from
        if number_to:
            params["numberTo"] = number_to
        if start_from:
            params["startFrom"] = start_from
        if start_to:
            params["startTo"] = start_to
        if end_from:
            params["endFrom"] = end_from
        if end_to:
            params["endTo"] = end_to
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)
