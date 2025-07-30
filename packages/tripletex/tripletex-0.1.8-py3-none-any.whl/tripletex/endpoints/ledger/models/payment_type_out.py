"""Data models for Tripletex payment type out endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class PaymentTypeOut(BaseModel):
    """
    Represents a payment type out in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        name: Payment type name.
        description: Payment type description.
        display_name: User-friendly display name.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")

    model_config = ConfigDict(populate_by_name=True)


class PaymentTypeOutResponse(TripletexResponse[PaymentTypeOut]):
    """Response wrapper for a list of PaymentTypeOut objects."""
