from typing import List, Optional, Type, Union

from crudclient.types import JSONDict  # Changed import to crudclient.types
from pydantic import BaseModel

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models.internal_match import (
    ReconciliationMatch,
    ReconciliationMatchResponse,
)


class TripletexBankReconciliationInternalMatch(TripletexCrud[ReconciliationMatch]):
    _resource_path = "internal/match"
    _datamodel = ReconciliationMatch
    _api_response_model = ReconciliationMatchResponse
    # Only list and destroy are standard. Others are custom or direct client calls.
    allowed_actions = ["list", "destroy"]

    def list_matches(
        self,
        parent_id: str,  # bankReconciliationId
        approved: Optional[bool] = None,
        query: Optional[str] = None,
        count: Optional[int] = None,
        from_: Optional[int] = None,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> ReconciliationMatchResponse:
        params: JSONDict = {}
        if approved is not None:
            params["approved"] = approved
        if query is not None:
            params["query"] = query
        if count is not None:
            params["count"] = count
        if from_ is not None:
            params["from"] = from_
        if sorting is not None:
            params["sorting"] = sorting
        if fields is not None:
            params["fields"] = fields

        # The parent_id for self.list() is the bankReconciliationId
        response = self.list(parent_id=parent_id, params=params)
        return self._convert_dict_to_model(response, self._api_response_model)  # type: ignore

    def create_match(self, parent_id: str, data: ReconciliationMatch) -> None:
        """POST /bank/reconciliation/{parent_id}/internal/match"""
        dumped_data = self._dump_data(data, partial=False)  # model and exclude_unset removed
        # Expects 200 OK with no content, client.post handles parsing
        self.client.post(path=self._get_endpoint(parent_id=parent_id), json=dumped_data)
        return None

    def delete_match(self, parent_id: str, match_id: int) -> None:
        """DELETE /bank/reconciliation/{parent_id}/internal/match/{match_id}"""
        self.destroy(resource_id=str(match_id), parent_id=parent_id)
        return None

    def update_suggestions(self, parent_id: str, data: List[ReconciliationMatch], approve: bool) -> None:
        """PUT /bank/reconciliation/{parent_id}/internal/match/updateSuggestions"""
        dumped_list = [self._dump_data(item, partial=False) for item in data]  # model and exclude_unset removed, assuming full objects for list items
        params = {"approve": approve}
        # Expects 200 OK with no content
        self.custom_action(
            action="updateSuggestions",
            method="put",
            parent_id=parent_id,
            data=dumped_list,
            params=params,
        )
        return None

    def update_multiple_matches(
        self,
        parent_id: str,
        data: List[ReconciliationMatch],
        # bank_reconciliation_id: Optional[int] = None, # This is parent_id
        approved: Optional[bool] = None,
        query: Optional[str] = None,
        count: Optional[int] = None,
    ) -> ReconciliationMatchResponse:
        """PUT /bank/reconciliation/{parent_id}/internal/match"""
        params: JSONDict = {}
        # if bank_reconciliation_id is not None: # Covered by parent_id
        #     params["bankReconciliationId"] = bank_reconciliation_id
        if approved is not None:
            params["approved"] = approved
        if query is not None:
            params["query"] = query
        if count is not None:
            params["count"] = count

        dumped_list = [self._dump_data(item, partial=False) for item in data]  # model and exclude_unset removed, assuming full objects for list items
        response_data = self.client.put(path=self._get_endpoint(parent_id=parent_id), json=dumped_list, params=params)
        return self._convert_dict_to_model(response_data, self._api_response_model)  # type: ignore

    def run_auto_match_algorithm(self, parent_id: str) -> ReconciliationMatchResponse:  # This is the bankReconciliationId from query param
        """PUT /bank/reconciliation/{parent_id}/internal/match/runAutoMatchAlgorithm"""
        params = {"bankReconciliationId": parent_id}  # API spec has bankReconciliationId as query param
        # even though it's also in the path via parent_id.
        # custom_action will build path with parent_id.
        # We pass bankReconciliationId in params as per spec for this action.

        response_data = self.custom_action(
            action="runAutoMatchAlgorithm",
            method="put",
            parent_id=parent_id,  # Used for path construction
            params=params,  # Query parameters for the action
        )
        return self._convert_dict_to_model(response_data, self._api_response_model)  # type: ignore

    def _convert_dict_to_model(self, data: Union[JSONDict, List[JSONDict]], model_type: Type[BaseModel]) -> Union[BaseModel, List[BaseModel]]:
        # Helper to ensure correct model conversion, as custom_action/client calls return JSONDict
        if model_type is None:
            raise ValueError("model_type cannot be None for _convert_dict_to_model")

        if isinstance(data, list):
            return [model_type(**item) for item in data]
        # Ensure data is a dict before passing to model_type
        if not isinstance(data, dict):
            # This case should ideally not happen if API returns valid JSON dicts
            # or client methods handle "no content" by returning empty dict or specific type.
            # If data is, e.g. None or an empty string from a malformed response:
            raise TypeError(f"Expected dict for model conversion, got {type(data)}")
        return model_type(**data)
