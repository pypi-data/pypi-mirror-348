"""Data models for Tripletex Close Group endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import Change, IdUrl, TripletexResponse


class CloseGroup(BaseModel):
    """
    Represents a group of postings that are closed together (e.g., payment matching).

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        date: Date of the closing action.
        postings: List of postings included in this close group.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    date: Optional[str] = None
    postings: Optional[List[IdUrl]] = None

    model_config = ConfigDict(populate_by_name=True)


class CloseGroupCreate(BaseModel):
    """
    Model for creating a new close group.

    Attributes:
        date: Date of the closing action (YYYY-MM-DD).
        postings: List of posting IDs to include in this close group.
    """

    date: str
    postings: List[IdUrl]

    model_config = ConfigDict(populate_by_name=True)


class CloseGroupResponse(TripletexResponse[CloseGroup]):
    """Response wrapper for a list of CloseGroup objects."""
