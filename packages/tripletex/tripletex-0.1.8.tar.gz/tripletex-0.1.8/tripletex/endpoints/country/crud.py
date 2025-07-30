from typing import ClassVar, List, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.country.models import Country, CountryResponse


class TripletexCountries(TripletexCrud[Country]):
    _resource_path: ClassVar[str] = "country"
    _datamodel: ClassVar[Type[Country]] = Country
    _api_response_model: ClassVar[Type[CountryResponse]] = CountryResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read"]
    _list_return_keys: ClassVar[List[str]] = ["values"]
