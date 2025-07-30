from typing import ClassVar, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.core.models import IdRef
from tripletex.endpoints.ledger.models import (
    Posting,
    PostingCreate,
    PostingResponse,
    PostingUpdate,
)

from .ledger import TripletexLedger


class TripletexPosting(TripletexCrud[Posting]):
    """API methods for interacting with ledger postings."""

    _resource_path: ClassVar[str] = "posting"
    _datamodel: ClassVar[Type[Posting]] = Posting
    _create_model: ClassVar[Type[PostingCreate]] = PostingCreate
    _update_model: ClassVar[Type[PostingUpdate]] = PostingUpdate
    _api_response_model: ClassVar[Type[PostingResponse]] = PostingResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None) -> PostingResponse:
        """
        List postings.

        Note: The Tripletex API requires 'dateFrom' and 'dateTo' parameters for this endpoint.
              If not provided in 'params', this method will default to yesterday and today.

        Args:
            parent_id: Optional parent ID if this is a nested resource.
            params: Optional query parameters. Should include 'dateFrom' and 'dateTo'.
                    Other common params: 'count', 'from', 'accountId', 'voucherId'.

        Returns:
            PostingResponse object containing a list of postings and potential metadata.
        """
        from tripletex.utils import ensure_date_params

        # Ensure required date parameters are present, defaulting if necessary
        params = ensure_date_params(params)

        # Call the base list method, which should return the _api_response_model instance
        return super().list(parent_id=parent_id, params=params)

    def search_open_posts(
        self,
        date: Optional[str] = None,
        account_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        project_id: Optional[int] = None,
        product_id: Optional[int] = None,
        account_number_from: Optional[int] = None,
        account_number_to: Optional[int] = None,
        from_index: Optional[int] = None,
        count: Optional[int] = None,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
        params: Optional[JSONDict] = None,
    ) -> PostingResponse:
        """
        Find open posts corresponding with sent data. Uses the custom action endpoint GET /ledger/posting/openPost.

        This method can be called in two ways:
        1. With individual parameters (date, account_id, etc.)
        2. With a params dictionary containing all parameters

        Args:
            date: Invoice date in yyyy-MM-dd format (required if params not provided)
            account_id: Element ID for filtering
            supplier_id: Element ID for filtering
            customer_id: Element ID for filtering
            employee_id: Element ID for filtering
            department_id: Element ID for filtering
            project_id: Element ID for filtering
            product_id: Element ID for filtering
            account_number_from: Element ID for filtering
            account_number_to: Element ID for filtering
            from_index: From index (default 0)
            count: Number of elements to return (default 1000)
            sorting: Sorting pattern
            fields: Fields filter pattern
            parent_id: Optional parent ID if this is a nested resource
            params: Optional dictionary of query parameters (alternative to individual parameters)

        Returns:
            PostingResponse object containing a list of open postings.
        """
        # Initialize params dictionary
        if params is None:
            params = {}
        else:
            # Create a copy to avoid modifying the original
            params = params.copy()

        assert date is not None or "date" in params, "Either 'date' or 'params['date']' must be provided."

        # Add individual parameters to params dictionary if provided
        # These take precedence over any values in the params dictionary
        if date is not None:
            params["date"] = date
        if account_id is not None:
            params["accountId"] = str(account_id)
        if supplier_id is not None:
            params["supplierId"] = str(supplier_id)
        if customer_id is not None:
            params["customerId"] = str(customer_id)
        if employee_id is not None:
            params["employeeId"] = str(employee_id)
        if department_id is not None:
            params["departmentId"] = str(department_id)
        if project_id is not None:
            params["projectId"] = str(project_id)
        if product_id is not None:
            params["productId"] = str(product_id)
        if account_number_from is not None:
            params["accountNumberFrom"] = str(account_number_from)
        if account_number_to is not None:
            params["accountNumberTo"] = str(account_number_to)
        if from_index is not None:
            params["from"] = str(from_index)
        if count is not None:
            params["count"] = str(count)
        if sorting is not None:
            params["sorting"] = sorting
        if fields is not None:
            params["fields"] = fields

        # The openPost endpoint returns a response that already has the structure we need
        # We just need to use the client directly to get the raw response
        endpoint = self._get_endpoint("openPost")
        raw_response = self.client.get(endpoint, params=params)

        # The raw_response is already a dictionary with the structure we need
        # We just need to convert it to a PostingResponse object
        return self._api_response_model.model_validate(raw_response)

    @staticmethod
    def create_entity_posting(
        row: int,
        description: str,
        account_id: str,
        amount: float,
        entity_type: str,
        entity_id: int,
    ) -> PostingCreate:
        """
        Create a posting model instance for a specific entity type (customer or supplier).

        Args:
            row: Row number for the posting.
            description: Description of the posting.
            account_id: Id of the account.
            amount: Amount for the posting.
            entity_type: Type of entity ('customer' or 'supplier').
            entity_id: ID of the entity (customer or supplier).

        Returns:
            PostingCreate: A posting model instance with the appropriate entity field set.

        Raises:
            ValueError: If entity_type is not 'customer' or 'supplier', or if entity_id is None.
        """
        if entity_type not in ["customer", "supplier"]:
            raise ValueError("Entity type must be either 'customer' or 'supplier'")

        if entity_id is None:
            raise ValueError(f"{entity_type.capitalize()} ID is missing")

        kwargs = {"row": row, "description": description, "account": IdRef(id=account_id), "amount": amount, entity_type: IdRef(id=entity_id)}

        return PostingCreate(**kwargs)

    # The create_customer_posting and create_supplier_posting methods have been
    # consolidated into the create_entity_posting method above.
    # Use create_entity_posting with entity_type="customer" or entity_type="supplier"
