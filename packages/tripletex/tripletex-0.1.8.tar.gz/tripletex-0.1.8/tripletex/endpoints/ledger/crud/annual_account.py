from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    AnnualAccount,
    AnnualAccountResponse,
)

from .ledger import TripletexLedger


class TripletexAnnualAccount(TripletexCrud[AnnualAccount]):
    """API methods for interacting with ledger annual accounts."""

    _resource_path: ClassVar[str] = "annualAccount"
    _datamodel: ClassVar[Type[AnnualAccount]] = AnnualAccount
    _api_response_model: ClassVar[Type[AnnualAccountResponse]] = AnnualAccountResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        id: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> AnnualAccountResponse:
        """
        Find annual accounts corresponding with sent data.

        Args:
            id: List of IDs
            year_from: From and including
            year_to: To and excluding
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            AnnualAccountResponse containing a list of AnnualAccount objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if year_from:
            params["yearFrom"] = year_from
        if year_to:
            params["yearTo"] = year_to
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)
