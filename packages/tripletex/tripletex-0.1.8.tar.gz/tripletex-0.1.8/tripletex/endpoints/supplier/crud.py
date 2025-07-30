from typing import ClassVar, List, Optional, Type

from crudclient.exceptions import MultipleResourcesFoundError, NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import (
    Supplier,
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)


class TripletexSuppliers(TripletexCrud[Supplier]):
    """API endpoint for managing suppliers in Tripletex."""

    _resource_path: ClassVar[str] = "supplier"
    _datamodel: ClassVar[Type[Supplier]] = Supplier
    _create_model: ClassVar[Type[SupplierCreate]] = SupplierCreate
    _update_model: ClassVar[Type[SupplierUpdate]] = SupplierUpdate
    _api_response_model: ClassVar[Type[SupplierResponse]] = SupplierResponse
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update", "destroy"]

    def search(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        supplier_number: Optional[str] = None,
        organization_number: Optional[str] = None,
        email: Optional[str] = None,
        invoice_email: Optional[str] = None,
        is_inactive: Optional[bool] = None,
        account_manager_id: Optional[str] = None,
        changed_since: Optional[str] = None,
        is_wholesaler: Optional[bool] = None,
        show_products: Optional[bool] = None,
        is_supplier: Optional[bool] = None,
        is_customer: Optional[bool] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> SupplierResponse:
        """
        Find suppliers corresponding with sent data.

        Args:
            id: List of IDs
            name: Supplier name
            supplier_number: Supplier number
            organization_number: Organization number
            email: Email address
            invoice_email: Invoice email address
            is_inactive: Is inactive
            account_manager_id: Account manager ID
            changed_since: Only return elements that have changed since this date and time
            is_wholesaler: Is wholesaler
            show_products: Show products
            is_supplier: Is supplier
            is_customer: Is customer
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            SupplierResponse object containing a list of Supplier objects.
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if supplier_number:
            params["supplierNumber"] = supplier_number
        if organization_number:
            params["organizationNumber"] = organization_number
        if email:
            params["email"] = email
        if invoice_email:
            params["invoiceEmail"] = invoice_email
        if is_inactive is not None:
            params["isInactive"] = is_inactive
        if account_manager_id:
            params["accountManagerId"] = account_manager_id
        if changed_since:
            params["changedSince"] = changed_since
        if is_wholesaler is not None:
            params["isWholesaler"] = is_wholesaler
        if show_products is not None:
            params["showProducts"] = show_products
        if is_supplier is not None:
            params["isSupplier"] = is_supplier
        if is_customer is not None:
            params["isCustomer"] = is_customer
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # self.list() is expected to return the ResponseObject if _api_response_model is set
        response_obj = self.list(params=params)  # self.list() from base Crud
        # Ensure it's the expected response type, using self._api_response_model for genericness
        if not isinstance(response_obj, self._api_response_model):
            raise TypeError(f"Expected {self._api_response_model.__name__} from list, got {type(response_obj)}")
        return response_obj

    def get_by_name_or_404(self, name: str) -> Supplier:
        """
        Retrieve a single supplier by its name.

        Args:
            name: The supplier name to search for.

        Returns:
            The Supplier object if found.

        Raises:
            NotFoundError: If no supplier with the given name is found.
            MultipleResourcesFoundError: If multiple suppliers with the given name are found.
        """
        response_obj = self.search(name=name, count=2)
        suppliers_list = response_obj.values if hasattr(response_obj, "values") else []

        if not suppliers_list:
            raise NotFoundError(f"No supplier found with name '{name}'.")
        if len(suppliers_list) == 1:
            return suppliers_list[0]
        raise MultipleResourcesFoundError(f"Multiple suppliers ({len(suppliers_list)}) found with name '{name}'. Expected exactly one.")

    def get_by_organization_number_or_404(self, organization_number: str) -> Supplier:
        """
        Retrieve a single supplier by its organization number.

        Args:
            organization_number: The organization number to search for.

        Returns:
            The Supplier object if found.

        Raises:
            NotFoundError: If no supplier with the given organization number is found.
            MultipleResourcesFoundError: If multiple suppliers with the given organization number are found.
        """
        response_obj = self.search(organization_number=organization_number, count=2)
        suppliers_list = response_obj.values if hasattr(response_obj, "values") else []

        if not suppliers_list:
            raise NotFoundError(f"No supplier found with organization number '{organization_number}'.")
        if len(suppliers_list) == 1:
            return suppliers_list[0]
        raise MultipleResourcesFoundError(
            f"Multiple suppliers ({len(suppliers_list)}) found with organization number '{organization_number}'. Expected exactly one."
        )

    def get_supplier_by_organization_number_or_name_or_404(self, name: Optional[str] = None, organization_number: Optional[str] = None) -> Supplier:
        """
        Finds a single supplier using a prioritized search, expecting an exact match.
        1. By organization number (if provided).
        2. By name (if provided and organization number search did not yield a result or was not performed).

        Args:
            name: The name of the supplier.
            organization_number: The organization number of the supplier.

        Returns:
            The found Supplier object.

        Raises:
            ValueError: If neither name nor organization_number is provided.
            NotFoundError: If no supplier is found by the specified criteria (0 results).
            MultipleResourcesFoundError: If multiple suppliers are found by the specified criteria (>1 result).
        """
        if not name and not organization_number:
            raise ValueError("Either name or organization_number must be provided to get_supplier_by_organization_number_or_name_or_404")

        last_error: Optional[Exception] = None

        # Attempt 1: By organization number
        if organization_number:
            try:
                # get_by_organization_number_or_404 will raise NotFoundError or MultipleResourcesFoundError
                return self.get_by_organization_number_or_404(organization_number)
            except MultipleResourcesFoundError:
                raise  # Propagate if multiple are found by org number
            except NotFoundError as e:
                last_error = e  # Store error if 0 found
                if not name:  # If only org number was given and it failed (0 found)
                    raise  # Re-raise this NotFoundError

        # Attempt 2: By name
        # This is reached if:
        # - organization_number was not provided, OR
        # - organization_number was provided but resulted in NotFoundError (0 found)
        if name:  # this will always be true if we reach this point
            try:
                # get_by_name_or_404 will raise NotFoundError or MultipleResourcesFoundError
                return self.get_by_name_or_404(name)
            except MultipleResourcesFoundError:
                raise  # Propagate if multiple are found by name
            except NotFoundError as e:
                last_error = e  # Store error if 0 found by name

        # If we've reached here, all applicable searches failed to find a unique supplier,
        # or found 0 results in the last applicable search.
        if last_error:  # This will be the NotFoundError from the last failed attempt (0 results)
            # Construct a more informative message based on what was attempted
            criteria_parts = []
            if organization_number:
                criteria_parts.append(f"organization number '{organization_number}'")
            if name:
                criteria_parts.append(f"name '{name}'")
            criteria_str = " or ".join(criteria_parts)
            raise NotFoundError(f"No supplier found using {criteria_str} after all attempts.") from last_error

        # Fallback, though theoretically covered by the logic above.
        raise NotFoundError("Supplier lookup failed: No criteria led to a unique supplier after all attempts.")
