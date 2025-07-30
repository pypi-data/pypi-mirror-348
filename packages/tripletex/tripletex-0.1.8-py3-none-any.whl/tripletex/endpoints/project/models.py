from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from tripletex.core.models import IdRef, IdUrl, TripletexResponse
from tripletex.endpoints.employee.models import Employee


# Base model with common fields used in Create, Update, and Response
class ProjectBase(BaseModel):
    """
    Base model with common fields used in Create, Update, and Response
    """

    name: str
    """The name of the project."""
    number: Optional[str] = None
    """The project number."""
    start_date: Optional[date] = Field(None, alias="startDate")
    """The start date of the project."""
    end_date: Optional[date] = Field(None, alias="endDate")
    """The end date of the project."""
    is_closed: Optional[bool] = Field(None, alias="isClosed")
    """Flag indicating if the project is closed."""
    is_offer: Optional[bool] = Field(None, alias="isOffer")
    """Flag indicating if the project is an offer."""
    is_fixed_price: Optional[bool] = Field(None, alias="isFixedPrice")
    """Flag indicating if the project has a fixed price."""
    # Note: Add other common fields if identified


# Model for creating a project (Payload for POST)
# Does NOT inherit from ProjectBase as API rejects fields like customerId, projectManagerId etc. on create
class ProjectCreate(BaseModel):
    """
    Data model for creating a new project.
    Does NOT inherit from ProjectBase as API rejects fields like customerId, projectManagerId etc. on create
    """

    name: str
    """The name of the project."""
    number: Optional[str] = None
    """The project number."""
    project_manager: IdRef = Field(..., alias="projectManager")
    """Reference (IdRef) to the project manager (employee). Required for creation."""
    # Note: Only include fields explicitly allowed/required by POST /v2/project


# Model for updating a project (Payload for PUT)
# Assuming PUT requires all fields similar to Create
class ProjectUpdate(ProjectCreate):
    """
    Data model for updating an existing project. Inherits fields from ProjectCreate.
    """


# Model representing a project as returned by the API (Response for GET, POST, PUT)
class Project(ProjectBase):
    """
    Data model representing a project, including read-only fields like ID and version.
    Inherits common fields from ProjectBase.
    """

    id: int
    """The unique identifier of the project."""
    version: int
    """The version number for optimistic locking."""
    # Optional related objects often returned by GET requests
    # Use IdUrl or specific models depending on API response structure
    customer: Optional[IdUrl] = None
    """The associated customer object (likely an IdUrl link, if requested/available)."""
    project_manager: Optional[Employee] = Field(None, alias="projectManager")
    """The associated project manager (employee) object (if requested/available)."""
    department: Optional[IdUrl] = None
    """The associated department object (represented by IdUrl, if requested/available)."""
    # Note: Add other fields returned by GET /project/{id} if known


class ProjectResponse(TripletexResponse[Project]):
    """
    Response model for project list endpoints.
    Wraps a list of Project objects in the standard Tripletex response format.
    """
