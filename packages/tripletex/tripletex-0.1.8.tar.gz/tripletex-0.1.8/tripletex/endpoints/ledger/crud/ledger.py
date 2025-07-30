from typing import ClassVar, Optional, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import LedgerAccount, LedgerAccountResponse


class TripletexLedger(TripletexCrud[LedgerAccount]):
    """API methods for interacting with the main ledger."""

    _resource_path: ClassVar[str] = "ledger"
    _datamodel: ClassVar[Type[LedgerAccount]] = LedgerAccount
    _api_response_model: ClassVar[Type[LedgerAccountResponse]] = LedgerAccountResponse

    def search(
        self,
        date_from: str,
        date_to: str,
        open_postings: Optional[str] = None,
        account_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        project_id: Optional[int] = None,
        product_id: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> LedgerAccountResponse:
        """
        Get ledger (hovedbok).

        Args:
            date_from: Format is yyyy-MM-dd (from and incl.)
            date_to: Format is yyyy-MM-dd (to and excl.)
            open_postings: Deprecated
            account_id: Element ID for filtering
            supplier_id: Element ID for filtering
            customer_id: Element ID for filtering
            employee_id: Element ID for filtering
            department_id: Element ID for filtering
            project_id: Element ID for filtering
            product_id: Element ID for filtering
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern (note: 'date' is not a valid sorting field)
            fields: Fields filter pattern

        Returns:
            LedgerAccountResponse object containing the search results
        """
        params = {"dateFrom": date_from, "dateTo": date_to, "from": from_index, "count": count}

        if open_postings:
            params["openPostings"] = open_postings
        if account_id:
            params["accountId"] = account_id
        if supplier_id:
            params["supplierId"] = supplier_id
        if customer_id:
            params["customerId"] = customer_id
        if employee_id:
            params["employeeId"] = employee_id
        if department_id:
            params["departmentId"] = department_id
        if project_id:
            params["projectId"] = project_id
        if product_id:
            params["productId"] = product_id
        if sorting:
            # Note that 'date' is not a valid sorting field according to test results
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def open_post(
        self,
        date: str,
        account_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        project_id: Optional[int] = None,
        product_id: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> LedgerAccountResponse:
        """
        Find open posts corresponding with sent data.

        Args:
            date: Invoice date. Format is yyyy-MM-dd (to and excl.)
            account_id: Element ID for filtering
            supplier_id: Element ID for filtering
            customer_id: Element ID for filtering
            employee_id: Element ID for filtering
            department_id: Element ID for filtering
            project_id: Element ID for filtering
            product_id: Element ID for filtering
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern (note: 'date' is not a valid sorting field)
            fields: Fields filter pattern

        Returns:
            LedgerAccountResponse object containing the open posts
        """
        params = {"date": date, "from": from_index, "count": count}

        if account_id:
            params["accountId"] = account_id
        if supplier_id:
            params["supplierId"] = supplier_id
        if customer_id:
            params["customerId"] = customer_id
        if employee_id:
            params["employeeId"] = employee_id
        if department_id:
            params["departmentId"] = department_id
        if project_id:
            params["projectId"] = project_id
        if product_id:
            params["productId"] = product_id
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.custom_action("openPost", method="get", params=params)
