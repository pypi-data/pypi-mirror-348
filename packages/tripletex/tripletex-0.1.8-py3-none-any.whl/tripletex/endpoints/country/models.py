from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class Country(BaseModel):
    """
    Represents a country entity in Tripletex.

    Attributes:
        id: Unique identifier for the country.
        version: Version number of the country record.
        changes: List of changes made to the country record.
        url: URL pointing to the country resource.
        name: The official name of the country.
        display_name: A user-friendly display name for the country.
        iso_alpha_2_code: The ISO 3166-1 alpha-2 code (e.g., "NO").
        iso_alpha_3_code: The ISO 3166-1 alpha-3 code (e.g., "NOR").
        iso_numeric_code: The ISO 3166-1 numeric code (e.g., "578").
        additional_properties: Allows for any additional properties returned by the API.
    """

    id: int
    version: int
    changes: Optional[List[Change]] = None
    url: str
    name: str
    display_name: Optional[str] = Field(None, alias="displayName")
    iso_alpha_2_code: Optional[str] = Field(None, alias="isoAlpha2Code")
    iso_alpha_3_code: Optional[str] = Field(None, alias="isoAlpha3Code")
    iso_numeric_code: Optional[str] = Field(None, alias="isoNumericCode")
    additional_properties: dict[str, Any] = {}

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class CountryResponse(TripletexResponse[Country]):
    """Response wrapper for a list of Country objects."""
