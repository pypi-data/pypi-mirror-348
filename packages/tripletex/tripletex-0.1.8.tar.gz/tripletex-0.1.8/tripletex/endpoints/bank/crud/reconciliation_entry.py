from typing import Any, ClassVar, List, Optional, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.bank.models import (
    BankReconciliationEntryBankTransaction,
    BankReconciliationEntryBankTransactionResponse,
    ReconciliationEntry,
)


class TripletexBankReconciliationEntry(TripletexCrud[BankReconciliationEntryBankTransaction]):
    """API endpoint for accessing bank reconciliation entry in Tripletex."""

    _resource_path: ClassVar[str] = "entry"
    _datamodel: ClassVar[Type[BankReconciliationEntryBankTransaction]] = BankReconciliationEntryBankTransaction
    _api_response_model: ClassVar[Type[BankReconciliationEntryBankTransactionResponse]] = BankReconciliationEntryBankTransactionResponse
    allowed_actions: ClassVar[List[str]] = []  # No standard CRUD operations allowed

    def update_bank_transaction(
        self,
        bank_transaction_ids: List[int],
        reconciliation_id: int,
    ) -> BankReconciliationEntryBankTransaction:
        """
        Update bank transactions for a reconciliation entry.

        Args:
            bank_transaction_ids: List of bank transaction IDs to update
            reconciliation_id: ID of the reconciliation

        Returns:
            BankReconciliationEntryBankTransaction object with the updated bank transactions.
        """
        data = BankReconciliationEntryBankTransaction(
            bank_transaction_ids=bank_transaction_ids,
            reconciliation_id=reconciliation_id,
        )

        # Use custom_action for the bankTransaction endpoint with PUT method
        response_obj = self.custom_action(
            action="bankTransaction",
            method="put",
            data=data,
        )

        # Ensure it's the expected response type
        if not isinstance(response_obj, self._datamodel):
            raise TypeError(f"Expected {self._datamodel.__name__}, got {type(response_obj)}")

        return response_obj

    def _build_update_posting_query_params(
        self,
        account_id: int,
        start_date: Optional[str],
        query: Optional[str],
        entry_type: Optional[str],
        sort_order: str,
        sort_field: str,
    ) -> str:
        """Build the query string for updating postings."""
        query_params = [f"accountId={account_id}"]
        if start_date is not None:
            query_params.append(f"startDate={start_date}")
        if query is not None:
            query_params.append(f"query={query}")
        if entry_type is not None:
            query_params.append(f"entryType={entry_type}")
        query_params.append(f"sortOrder={sort_order}")
        query_params.append(f"sortField={sort_field}")
        return "&".join(query_params)

    def _process_update_posting_response(self, response: Any) -> List[ReconciliationEntry]:
        """Process the response from updating postings."""
        entries_result: List[ReconciliationEntry] = []
        items_to_process = []

        if isinstance(response, dict) and "values" in response:
            items_to_process = response["values"]
        elif isinstance(response, list):
            items_to_process = response

        for item in items_to_process:
            if isinstance(item, dict):
                entries_result.append(ReconciliationEntry(**item))
            elif isinstance(item, ReconciliationEntry):
                entries_result.append(item)
        return entries_result

    def update_posting(
        self,
        posting_ids: List[int],
        account_id: int,
        start_date: Optional[str] = None,
        query: Optional[str] = None,
        entry_type: Optional[str] = None,
        sort_order: str = "ascending",
        sort_field: str = "date",
    ) -> List[ReconciliationEntry]:
        """
        Find reconciliation postings corresponding with sent data.

        Args:
            posting_ids: List of posting IDs to update
            account_id: ID of the account
            start_date: Optional start date filter
            query: Optional search query
            entry_type: Optional entry type filter (POSTING or BANK_TRANSACTION)
            sort_order: Sort order, default is 'ascending'
            sort_field: Field to sort by, default is 'date'

        Returns:
            List of ReconciliationEntry objects matching the criteria.
        """
        entries_payload = [{"id": posting_id, "entryType": "Posting"} for posting_id in posting_ids]

        query_string = self._build_update_posting_query_params(
            account_id=account_id,
            start_date=start_date,
            query=query,
            entry_type=entry_type,
            sort_order=sort_order,
            sort_field=sort_field,
        )

        endpoint = f"{self._get_endpoint('posting')}?{query_string}"
        response = self.client.put(endpoint, json=entries_payload)

        return self._process_update_posting_response(response)
