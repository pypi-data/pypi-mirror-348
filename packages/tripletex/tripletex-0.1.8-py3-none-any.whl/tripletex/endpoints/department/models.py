from typing import Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import TripletexResponse


class Department(BaseModel):
    """Represents a department resource in Tripletex."""

    id: int
    version: int
    url: str
    name: str
    model_config = ConfigDict(populate_by_name=True)


class DepartmentCreate(BaseModel):
    """Data required to create a new department."""

    name: str


class DepartmentUpdate(BaseModel):
    """Data allowed when updating an existing department."""

    name: Optional[str] = None


class DepartmentResponse(TripletexResponse[Department]):
    """Response wrapper for single department results."""
