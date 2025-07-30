# -*- coding: utf-8 -*-
from typing import ClassVar, Optional, Type

from crudclient.exceptions import DeprecatedEndpointError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.company.models import (
    Company,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)


class TripletexCompany(TripletexCrud[Company]):
    """API Logic for /company endpoint."""

    _resource_path: ClassVar[str] = "company"
    _datamodel: ClassVar[Type[Company]] = Company
    _update_model: ClassVar[Type[CompanyUpdate]] = CompanyUpdate
    _api_response_model: ClassVar[Type[CompanyResponse]] = CompanyResponse
    allowed_actions: ClassVar[list[str]] = ["read", "update"]
    _update_mode: str = "no_resource_id"

    def get_divisions(
        self,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> CompanyListResponse:
        """Fetch divisions for the company.
        GET /company/divisions

        DEPRECATED: This endpoint is fully deprecated and no longer works.

        Args:
            from_index: From index (for pagination). Default: 0.
            count: Number of elements to return. Default: 1000.
            sorting: Sorting pattern.
            fields: Fields filter pattern.

        Returns:
            CompanyListResponse: Response containing a list of divisions.

        Raises:
            DeprecatedEndpointError: This endpoint is deprecated and no longer works.
        """
        # Raise a DeprecatedEndpointError instead of making an actual request
        raise DeprecatedEndpointError("The company/divisions endpoint is deprecated and no longer works.")

    def get_with_login_access(
        self,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> CompanyListResponse:
        """Returns client customers (with accountant/auditor relation) where the current user has login access (proxy login).
        GET /company/>withLoginAccess

        Args:
            from_index: From index (for pagination). Default: 0.
            count: Number of elements to return. Default: 1000.
            sorting: Sorting pattern.
            fields: Fields filter pattern.

        Returns:
            CompanyListResponse: Response containing a list of companies.
        """
        # Prepare query parameters
        params: JSONDict = {"from": from_index, "count": count}
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Use the client's get method directly with the correct endpoint
        endpoint = self._get_endpoint(">withLoginAccess")
        response_data = self.client.get(endpoint, params=params)

        # Convert the response to a CompanyListResponse object
        return CompanyListResponse.model_validate(response_data)
