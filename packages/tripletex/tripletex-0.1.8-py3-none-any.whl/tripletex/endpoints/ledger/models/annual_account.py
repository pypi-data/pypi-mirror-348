"""Data models for Annual Account in Tripletex."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import Change, TripletexResponse


class AnnualAccount(BaseModel):
    """
    Represents an annual account (fiscal year) in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        year: The fiscal year.
        start: Start date of the fiscal year.
        end: End date of the fiscal year.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    year: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class AnnualAccountResponse(TripletexResponse[AnnualAccount]):
    """Response wrapper for a list of AnnualAccount objects."""
