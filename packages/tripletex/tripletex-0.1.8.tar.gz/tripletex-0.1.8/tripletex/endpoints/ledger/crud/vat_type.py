from typing import ClassVar, List, Optional, Type

from crudclient.exceptions import NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import VatType, VatTypeResponse

from .ledger import TripletexLedger


class TripletexVatType(TripletexCrud[VatType]):
    """API methods for interacting with ledger VAT types."""

    _resource_path: ClassVar[str] = "vatType"
    _datamodel: ClassVar[Type[VatType]] = VatType
    _api_response_model: ClassVar[Type[VatTypeResponse]] = VatTypeResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    allowed_actions: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        name: Optional[str] = None,
        number: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> VatTypeResponse:
        """
        Find VAT types corresponding with sent data.

        Args:
            name: Containing
            number: VAT type number
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            VatTypeResponse containing a list of VatType objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if name:
            params["name"] = name
        if number:
            params["number"] = number
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def find_by_number_or_404(self, vat_type_number: str) -> VatType:
        """
        Retrieve a single VAT type by its number.

        Args:
            vat_type_number: The VAT type number to search for.

        Returns:
            The VatType object if found.

        Raises:
            NotFoundError: If exactly one VAT type with the given number is not found.
        """
        # Use count=2 to efficiently check if 0, 1, or >1 VAT types exist
        response = self.search(number=vat_type_number, count=2)

        if len(response.values) == 1:
            return response.values[0]
        else:
            raise NotFoundError(f"Expected 1 VAT type with number '{vat_type_number}', found {len(response.values)}")

    def create_relative_vat_type(self, name: str, vat_type_id: int, percentage: float) -> VatType:
        """
        Create a new relative VAT Type.

        These are used if the company has 'forholdsmessig fradrag for inngående MVA'.

        Args:
            name: VAT type name, max 8 characters
            vat_type_id: VAT type ID. The relative VAT type will behave like this VAT type,
                        except for the basis for calculating the VAT deduction.
            percentage: Basis percentage. This percentage will be multiplied with the transaction
                       amount to find the amount that will be the basis for calculating the deduction amount.

        Returns:
            The created VAT type
        """
        # Create a dictionary with the query parameters
        params = {"name": name, "vatTypeId": vat_type_id, "percentage": percentage}  # Pass as integer, not string  # Pass as float, not string

        # Build the endpoint URL
        endpoint = self._get_endpoint("createRelativeVatType")

        # Use the client's _request method directly
        response = self.client._request(method="PUT", endpoint=endpoint, params=params)

        # Process the response
        if isinstance(response, dict) and "value" in response:
            return self._datamodel.model_validate(response["value"])

        return self._datamodel.model_validate(response)
