import logging
from typing import ClassVar, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.project.models import Project, ProjectCreate, ProjectResponse, ProjectUpdate

logger = logging.getLogger(__name__)


class TripletexProjects(TripletexCrud[Project]):
    """
    Provides CRUD operations for the Tripletex Project endpoint.

    Inherits standard GET, POST, PUT, DELETE methods from TripletexCrud.
    """

    _resource_path: ClassVar[str] = "project"
    _datamodel: ClassVar[Type[Project]] = Project
    _create_model: ClassVar[Type[ProjectCreate]] = ProjectCreate
    _update_model: ClassVar[Type[ProjectUpdate]] = ProjectUpdate
    _api_response_model: ClassVar[Type[ProjectResponse]] = ProjectResponse

    # No need to override __init__ as the base TripletexCrud class already initializes
    # _response_strategy with the appropriate parameters

    # No need to override _dump_data as the base TripletexCrud class already handles
    # both dictionary and model instance inputs properly
