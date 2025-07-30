from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    PostingRules,
    PostingRulesResponse,
)

from .ledger import TripletexLedger


class TripletexPostingRules(TripletexCrud[PostingRules]):
    """API methods for interacting with ledger posting rules."""

    _resource_path: ClassVar[str] = "postingRules"
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list"]
    _datamodel: ClassVar[Type[PostingRules]] = PostingRules
    _api_response_model: ClassVar[Type[PostingRulesResponse]] = PostingRulesResponse

    def get(self, fields: Optional[str] = None) -> PostingRules:
        """
        Get posting rules for current company.

        Args:
            fields: Fields filter pattern

        Returns:
            PostingRules object
        """
        params: JSONDict = {}
        if fields:
            params["fields"] = fields

        return self.custom_action("", method="get", params=params)
