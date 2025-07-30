"""Stub file for the Tripletex Department API endpoint."""

from typing import ClassVar, List, Type

from tripletex.core.crud import TripletexCrud

from .models import Department, DepartmentCreate, DepartmentResponse, DepartmentUpdate


class TripletexDepartments(TripletexCrud[Department]):
    """
    API endpoint for managing departments in Tripletex.

    Provides standard CRUD operations (list, read, create, update, destroy)
    for departments, inheriting base functionality from TripletexCrud.
    """

    _resource_path: ClassVar[str] = "department"
    _datamodel: ClassVar[Type[Department]] = Department
    _create_model: ClassVar[Type[DepartmentCreate]] = DepartmentCreate
    _update_model: ClassVar[Type[DepartmentUpdate]] = DepartmentUpdate
    _api_response_model: ClassVar[Type[DepartmentResponse]] = DepartmentResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update", "destroy"]

    def __init__(self, *args, **kwargs):
        """Initialize the department endpoint, configuring the response strategy."""
        super().__init__(*args, **kwargs)
