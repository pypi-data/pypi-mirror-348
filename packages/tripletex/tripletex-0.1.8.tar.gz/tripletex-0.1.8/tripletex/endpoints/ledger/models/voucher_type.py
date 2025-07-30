"""Data models specific to the Tripletex Voucher Type endpoints."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class VoucherTypeCreate(BaseModel):
    """
    Model for creating a voucher type reference in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Optional version number.
        name: Optional name.
        display_name: Optional display name.
    """

    id: int
    version: Optional[int] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")

    model_config = ConfigDict(populate_by_name=True)


class VoucherType(BaseModel):
    """
    Represents a voucher type in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        name: Voucher type name.
        display_name: User-friendly display name.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")

    model_config = ConfigDict(populate_by_name=True)


class VoucherTypeResponse(TripletexResponse[VoucherType]):
    """Response wrapper for a list of VoucherType objects."""
