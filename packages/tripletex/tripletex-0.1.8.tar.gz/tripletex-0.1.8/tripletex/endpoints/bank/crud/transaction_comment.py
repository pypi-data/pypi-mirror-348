from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import (
    BankTransactionComment,
    BankTransactionCommentCreate,
    BankTransactionCommentResponse,
)


class TripletexBankTransactionComments(TripletexCrud[BankTransactionComment]):
    """API endpoint for accessing bank transaction comments in Tripletex."""

    _resource_path: ClassVar[str] = "bank/transaction/comment"
    _datamodel: ClassVar[Type[BankTransactionComment]] = BankTransactionComment
    _create_model: ClassVar[Type[BankTransactionCommentCreate]] = BankTransactionCommentCreate
    _api_response_model: ClassVar[Type[BankTransactionCommentResponse]] = BankTransactionCommentResponse
    allowed_actions: ClassVar[List[str]] = ["list", "create", "destroy"]

    def list_by_transaction(
        self,
        bank_transaction_id: int,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> BankTransactionCommentResponse:
        """
        Get comments for a specific bank transaction.

        Args:
            bank_transaction_id: ID of the bank transaction
            from_index: From index (pagination)
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            BankTransactionCommentResponse object containing a list of BankTransactionComment objects.
        """
        params: JSONDict = {
            "bankTransactionId": bank_transaction_id,
            "from": from_index,
            "count": count,
        }

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

    def create_for_transaction(
        self,
        bank_transaction_id: int,
        comment: str,
    ) -> BankTransactionComment:
        """
        Create a comment for a specific bank transaction.

        Args:
            bank_transaction_id: ID of the bank transaction
            comment: The comment text

        Returns:
            BankTransactionComment object representing the created comment.
        """
        data = BankTransactionCommentCreate(comment=comment)
        params: JSONDict = {"bankTransactionId": bank_transaction_id}

        return self.create(data=data, params=params)
