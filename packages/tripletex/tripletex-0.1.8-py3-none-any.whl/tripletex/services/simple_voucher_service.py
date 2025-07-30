import datetime

from tripletex.core.api import TripletexAPI
from tripletex.endpoints.ledger.models.voucher import Voucher
from tripletex.services.voucher_service import VoucherService


class SimpleVoucherService:
    """Service for creating simple, balanced vouchers."""

    def __init__(self, api_client: TripletexAPI):
        """Initialize the service with a Tripletex API client.

        Args:
            api_client: The Tripletex API client to use for API calls.
        """
        self.api_client = api_client
        self.voucher_service = VoucherService(api_client)

    def create_simple_voucher(
        self,
        description: str,
        date: datetime.datetime,
        debit_account_number: str,
        credit_account_number: str,
        amount: float,
        send_to_ledger: bool = False,
        voucher_type_code: str = "K",  # Default to "K" (Utgift)
    ) -> Voucher:
        """
        Creates a simple, balanced voucher with one debit and one credit posting.

        This service uses the general VoucherService under the hood.

        Args:
            description: Description for the voucher and its postings.
            date: Date of the voucher.
            debit_account_number: Account number for the debit posting.
            credit_account_number: Account number for the credit posting.
            amount: The amount for the transaction (will be positive for debit, negative for credit).
            send_to_ledger: Whether to send the voucher to the ledger immediately. Defaults to True.
            voucher_type_code: The code for the voucher type (e.g., "K" for Utgift, "B" for Bank).
                               Defaults to "K".

        Returns:
            The created Voucher object.
        """
        # Fetch the voucher type ID based on the provided code
        voucher_type_obj = self.api_client.ledger.voucher_type.get_by_code_or_404(code=voucher_type_code)
        actual_voucher_type_id = voucher_type_obj.id

        # Prepare postings data for VoucherService
        postings_data = [
            {
                "amount": amount,
                "accountnumber": debit_account_number,
                "description": description,
            },
            {
                "amount": -amount,  # Negative for credit
                "accountnumber": credit_account_number,
                "description": description,
            },
        ]

        # Call the underlying VoucherService to create the voucher
        created_voucher = self.voucher_service.make_voucher(
            description=description,
            date=date,
            filepath=None,  # No attachment for this simple service
            postings=postings_data,
            supplier_id=None,  # No supplier info for this simple service
            send_to_ledger=send_to_ledger,
            voucher_type_id=actual_voucher_type_id,
        )
        return created_voucher
