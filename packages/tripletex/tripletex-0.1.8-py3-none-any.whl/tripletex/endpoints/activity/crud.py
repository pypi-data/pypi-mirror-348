import logging
from typing import Any, ClassVar, List, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.activity.models import (
    Activity,
    ActivityCreate,
    ActivityResponse,
)

logger = logging.getLogger(__name__)


class TripletexActivities(TripletexCrud[Activity]):
    """Provides API methods for interacting with activities."""

    _resource_path: ClassVar[str] = "activity"
    _datamodel: ClassVar[Type[Activity]] = Activity
    _create_model: ClassVar[Type[ActivityCreate]] = ActivityCreate
    _api_response_model: ClassVar[Type[ActivityResponse]] = ActivityResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create"]

    # No need to override __init__ as the base TripletexCrud class already initializes
    # _response_strategy with the appropriate parameters

    # No need to override _dump_data as the base TripletexCrud class already handles
    # both dictionary and model instance inputs properly

    def for_time_sheet(self, project_id: int, **kwargs: Any) -> ActivityResponse:
        """
        Get activities that can be used on time sheets.
        GET /activity/>forTimeSheet

        Args:
            project_id: The ID of the project to get activities for.
            **kwargs: Additional query parameters such as:
                - employee_id: Optional employee ID filter
                - date: Optional date filter
                - from_: Starting index
                - count: Number of items to return
                - sorting: Sorting order
                - fields: Fields to include

        Returns:
            ActivityResponse: Response containing a list of activities.
        """
        # Ensure project_id is included in the parameters
        params = {"projectId": project_id, **kwargs}

        # Use custom_action for non-standard GET requests with the >forTimeSheet action
        response_data = self.custom_action(
            action=">forTimeSheet",
            method="get",
            params=params,
        )
        # Convert the response to an ActivityResponse object
        return ActivityResponse(**response_data)

    def create_list(self, activities: List[ActivityCreate], **kwargs: Any) -> ActivityResponse:
        """
        Create multiple activities at once.
        POST /activity/list

        Args:
            activities: List of ActivityCreate objects to create.
            **kwargs: Additional query parameters.

        Returns:
            ActivityResponse: Response containing the created activities.
        """
        # Convert the list of ActivityCreate objects to a list of dictionaries
        activities_data = [activity.model_dump(by_alias=True) for activity in activities]

        # Use the client's post method directly
        endpoint = f"{self._resource_path}/list"
        response_data = self.client.post(endpoint, json=activities_data, params=kwargs)

        # Convert the response to an ActivityResponse object
        return ActivityResponse(**response_data)
