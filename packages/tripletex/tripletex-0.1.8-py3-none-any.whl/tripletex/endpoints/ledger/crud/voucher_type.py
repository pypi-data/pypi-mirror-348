from typing import ClassVar, List, Optional, Type

from crudclient.exceptions import NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    VoucherType,
    VoucherTypeResponse,
)

from .ledger import TripletexLedger


class TripletexVoucherType(TripletexCrud[VoucherType]):
    """API methods for interacting with ledger voucher types."""

    _resource_path: ClassVar[str] = "voucherType"
    _datamodel: ClassVar[Type[VoucherType]] = VoucherType
    _api_response_model: ClassVar[Type[VoucherTypeResponse]] = VoucherTypeResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> VoucherTypeResponse:
        """
        Find voucher types corresponding with sent data.

        Args:
            name: Containing
            code: Voucher type code
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            VoucherTypeResponse containing a list of VoucherType objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if name:
            params["name"] = name
        if code:
            params["code"] = code
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def find_by_name_or_404(self, name: str) -> VoucherType:
        """
        Retrieve a single voucher type by its exact name.

        Args:
            name: The voucher type name to search for.

        Returns:
            The VoucherType object if found.

        Raises:
            NotFoundError: If exactly one voucher type with the given name is not found.
        """
        # Use search with count=2 to efficiently check if 0, 1, or >1 voucher types exist
        response = self.search(name=name, count=2)
        results = response.values

        if len(results) == 1:
            return results[0]
        else:
            raise NotFoundError(f"Expected 1 voucher type with name '{name}', found {len(results)}")

    def get_by_code_or_404(self, code: str) -> VoucherType:
        """
        Retrieve a single voucher type by its exact code.

        Args:
            code: The voucher type code to search for.

        Returns:
            The VoucherType object if found.

        Raises:
            NotFoundError: If exactly one voucher type with the given code is not found.
        """
        # Use search with count=2 to efficiently check if 0, 1, or >1 voucher types exist
        response = self.search(code=code, count=2)
        results = response.values

        if len(results) == 1:
            return results[0]
        else:
            raise NotFoundError(f"Expected 1 voucher type with code '{code}', found {len(results)}")
