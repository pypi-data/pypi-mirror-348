from typing import ClassVar, Optional, Type

from crudclient.exceptions import NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    Account,
    AccountCreate,
    AccountResponse,
    AccountUpdate,
)

from .ledger import TripletexLedger


class TripletexAccount(TripletexCrud[Account]):
    """API methods for interacting with ledger accounts."""

    _resource_path: ClassVar[str] = "account"
    _datamodel: ClassVar[Type[Account]] = Account
    _api_response_model: ClassVar[Type[AccountResponse]] = AccountResponse
    _create_model: ClassVar[Type[AccountCreate]] = AccountCreate
    _update_model: ClassVar[Type[AccountUpdate]] = AccountUpdate
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger

    def search(
        self,
        id: Optional[str] = None,
        number: Optional[str] = None,
        name: Optional[str] = None,
        is_bank_account: Optional[bool] = None,
        is_inactive: Optional[bool] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> AccountResponse:
        """
        Find accounts corresponding with sent data.

        Args:
            id: List of IDs
            number: Account number
            name: Account name
            is_bank_account: Is bank account
            is_inactive: Is inactive
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of Account objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if number:
            params["number"] = number
        if name:
            params["name"] = name
        if is_bank_account is not None:
            params["isBankAccount"] = is_bank_account
        if is_inactive is not None:
            params["isInactive"] = is_inactive
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def get_by_number_or_404(self, account_number: str) -> Account:
        """
        Retrieve a single account by its number.

        Args:
            account_number: The account number to search for.

        Returns:
            The Account object if found.

        Raises:
            NotFoundError: If exactly one account with the given number is not found.
        """
        # Use count=2 to efficiently check if 0, 1, or >1 accounts exist
        response = self.search(number=account_number, count=2)

        if len(response.values) == 1:
            return response.values[0]
        else:
            raise NotFoundError(f"Expected 1 account with number '{account_number}', found {len(response.values)}")
