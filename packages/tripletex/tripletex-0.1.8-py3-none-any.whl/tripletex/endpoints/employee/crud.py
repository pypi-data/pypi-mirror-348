"""API wrapper for the Tripletex employee endpoint."""

from typing import ClassVar, List, Type

from tripletex.core.crud import TripletexCrud

from .models import Employee, EmployeeCreate, EmployeeUpdate


class TripletexEmployees(TripletexCrud[Employee]):
    """Handles CRUD operations for Tripletex employees."""

    _resource_path: ClassVar[str] = "/employee"
    _datamodel: ClassVar[Type[Employee]] = Employee
    _create_model: ClassVar[Type[EmployeeCreate]] = EmployeeCreate
    _update_model: ClassVar[Type[EmployeeUpdate]] = EmployeeUpdate
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update"]
    _list_return_keys: ClassVar[List[str]] = ["values"]
