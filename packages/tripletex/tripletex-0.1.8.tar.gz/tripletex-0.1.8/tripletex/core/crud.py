import logging
from typing import Any, ClassVar, List, Optional, Type, TypeVar

from crudclient import Crud, JSONDict, RawResponse  # type: ignore[attr-defined]
from crudclient.exceptions import DataValidationError
from crudclient.response_strategies.default import DefaultResponseModelStrategy
from pydantic import ValidationError as PydanticValidationError

T = TypeVar("T")
logger = logging.getLogger(__name__)


class TripletexCrud(Crud[T]):
    """
    Tripletex-specific CRUD operations base class.
    Overrides response conversion to handle the 'value' wrapper in Tripletex responses.
    """

    # These are defined as class variables to match most subclasses
    _list_return_keys: ClassVar[List[str]] = ["values"]
    _api_response_model: ClassVar[Optional[Type]] = None
    _create_model: ClassVar[Optional[Type]] = None
    _update_model: ClassVar[Optional[Type]] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Explicitly configure the response strategy
        self._response_strategy = DefaultResponseModelStrategy(
            datamodel=self._datamodel, api_response_model=self._api_response_model, list_return_keys=self._list_return_keys
        )

    def _dump_data(self, data: Any, partial: bool = False) -> Any:
        model_to_use: Optional[type] = None
        if hasattr(self, "_update_model") and self._update_model and isinstance(data, self._update_model):
            model_to_use = self._update_model
            logger.debug("Using _update_model based on data type.")
        elif hasattr(self, "_create_model") and self._create_model and isinstance(data, self._create_model):
            model_to_use = self._create_model
            logger.debug("Using _create_model based on data type.")
        elif not partial and hasattr(self, "_create_model") and self._create_model:
            model_to_use = self._create_model
            logger.debug("Falling back to _create_model for non-partial dict.")
        elif partial and hasattr(self, "_update_model") and self._update_model:
            model_to_use = self._update_model
            logger.debug("Falling back to _update_model for partial dict.")

        if model_to_use:
            logger.debug(f"Attempting validation and dumping with {model_to_use.__name__} (partial={partial})")
            try:
                # Create an instance of the model with the data
                # This works for both Pydantic v1 and v2 without needing to call specific methods
                instance = model_to_use(**data) if isinstance(data, dict) else data

                # Use exclude_unset=True only when updating (partial=True implicitly handled by model_validate)
                # and the model being used is specifically the _update_model.
                use_exclude_unset = model_to_use == self._update_model

                # Use model_dump if available (Pydantic v2), otherwise fall back to dict
                if hasattr(instance, "model_dump"):
                    dumped_data = instance.model_dump(mode="json", by_alias=True, exclude_unset=use_exclude_unset)
                else:
                    dumped_data = instance.dict(by_alias=True, exclude_unset=use_exclude_unset)

                logger.debug(f"Data validated and dumped successfully using {model_to_use.__name__}")
                return dumped_data
            except PydanticValidationError as e:
                error_message = f"Data validation failed using {model_to_use.__name__}. Errors: {e}"
                logger.error(error_message)
                raise DataValidationError(error_message, data=data) from e
        else:
            logger.debug("No specific create/update model found/applicable, falling back to super()._dump_data")
            # Ensure super call passes along partial correctly
            return super()._dump_data(data, partial=partial)

    def _convert_to_model(self, data: RawResponse) -> T | JSONDict:
        """
        TripleTex-specific method to convert API response to data model.

        Extracts the actual data from the 'value' field if present,
        then converts it to the specified datamodel or returns the raw dictionary.

        Args:
            data: The raw response data from the API.

        Returns:
            An instance of the datamodel T or the raw JSON dictionary.

        Raises:
            ValueError: If the validated response data is not a dictionary.
        """
        validated_data = self._validate_response(data)

        if not isinstance(validated_data, dict):
            raise ValueError(f"Unexpected response type: {type(validated_data)}")

        cleaned_data = validated_data.get("value", validated_data)

        return self._datamodel(**cleaned_data) if self._datamodel else validated_data
