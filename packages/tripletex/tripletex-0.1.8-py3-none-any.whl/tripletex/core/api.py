import logging
import os

from crudclient import API  # type: ignore[attr-defined]

from tripletex.core.client import TripletexClient
from tripletex.core.config import TripletexConfig, TripletexTestConfig
from tripletex.endpoints.activity.crud import TripletexActivities
from tripletex.endpoints.bank.crud import (
    TripletexBankReconciliation,
    TripletexBankReconciliationEntry,
    TripletexBankReconciliationInternalMatch,
    TripletexBanks,
    TripletexBankStatements,
    TripletexBankStatementTransactions,
    TripletexBankTransactionComments,
)
from tripletex.endpoints.company.crud import TripletexCompany
from tripletex.endpoints.country.crud import TripletexCountries
from tripletex.endpoints.department.crud import TripletexDepartments
from tripletex.endpoints.employee.crud import TripletexEmployees
from tripletex.endpoints.ledger.crud import (
    TripletexAccount,
    TripletexAccountingPeriod,
    TripletexAnnualAccount,
    TripletexCloseGroup,
    TripletexLedger,
    TripletexPaymentTypeOut,
    TripletexPosting,
    TripletexPostingRules,
    TripletexVatType,
    TripletexVoucher,
    TripletexVoucherHistorical,
    TripletexVoucherOpeningBalance,
    TripletexVoucherType,
)
from tripletex.endpoints.project.crud import TripletexProjects
from tripletex.endpoints.supplier.crud import TripletexSuppliers

# Set up logging
logger = logging.getLogger(__name__)


class TripletexAPI(API):
    """
    Main API class for interacting with the Tripletex API.

    Provides access to various endpoints like countries, suppliers, and ledger functionalities.
    Handles client initialization and configuration.
    """

    client_class = TripletexClient

    def __init__(
        self,
        client: TripletexClient | None = None,
        client_config: TripletexConfig | TripletexTestConfig | None = None,
        debug: bool | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Tripletex API client.

        Args:
            client: An optional pre-configured TripletexClient instance. If provided, client_config is ignored.
            client_config: An optional configuration object (TripletexConfig or TripletexTestConfig).
                           Used only if 'client' is not provided. Defaults based on 'debug'.
            debug: If True, uses TripletexTestConfig by default when creating a client internally.
                   Defaults to False or DEBUG env var.
            **kwargs: Additional arguments passed to the base API class.
        """

        if debug is None:
            debug = os.environ.get("DEBUG", "0") == "1"
            logger.debug("Param debug=None, setting debug=environ.DEBUG from os.environ: %s", debug)

        # Determine the actual client_config to pass to super().__init__
        # _initialize_client is called by super().__init__ if a 'client' instance is not provided.
        effective_client_config = client_config
        if client is None:  # Only determine/override client_config if we are creating the client
            if effective_client_config:
                logger.debug("Using provided client_config: %r", effective_client_config)
            elif debug:
                effective_client_config = TripletexTestConfig()
                logger.debug("Using TripletexTestConfig due to debug=True: %r", effective_client_config)
            else:
                effective_client_config = TripletexConfig()
                logger.debug("Using default TripletexConfig: %r", effective_client_config)

        super().__init__(client=client, client_config=effective_client_config, **kwargs)

        if client:
            logger.debug("TripletexAPI initialized with a pre-configured client: %r", client)
        else:
            logger.debug(
                "TripletexAPI initialized. Client instance created by superclass with config: %r. " "Client instance: %r",
                effective_client_config,
                self.client,
            )

    def _register_endpoints(self) -> None:
        """Registers all available API endpoints as attributes."""
        self.activities = TripletexActivities(self.client)
        self.bank = TripletexBanks(self.client)
        self.bank.transaction_comment = TripletexBankTransactionComments(self.client, parent=self.bank)
        self.bank.reconciliation = TripletexBankReconciliation(self.client, parent=self.bank)
        self.bank.reconciliation.entry = TripletexBankReconciliationEntry(self.client, parent=self.bank.reconciliation)
        self.bank.reconciliation.internal_match = TripletexBankReconciliationInternalMatch(self.client, parent=self.bank.reconciliation)
        self.bank.statement = TripletexBankStatements(self.client, parent=self.bank)
        self.bank.statement.transaction = TripletexBankStatementTransactions(self.client, parent=self.bank.statement)
        self.company = TripletexCompany(self.client)  # Register the company endpoint
        self.country = TripletexCountries(self.client)
        self.departments = TripletexDepartments(client=self.client)
        self.suppliers = TripletexSuppliers(self.client)
        self.projects = TripletexProjects(self.client)
        self.employee = TripletexEmployees(self.client)
        # Ledger endpoints
        self.ledger = TripletexLedger(self.client)
        self.ledger.accounting_period = TripletexAccountingPeriod(self.client, parent=self.ledger)
        self.ledger.annual_account = TripletexAnnualAccount(self.client, parent=self.ledger)
        self.ledger.close_group = TripletexCloseGroup(self.client, parent=self.ledger)
        self.ledger.voucher_type = TripletexVoucherType(self.client, parent=self.ledger)
        self.ledger.posting_rules = TripletexPostingRules(self.client, parent=self.ledger)
        self.ledger.account = TripletexAccount(self.client, parent=self.ledger)
        self.ledger.payment_type_out = TripletexPaymentTypeOut(self.client, parent=self.ledger)
        self.ledger.posting = TripletexPosting(self.client, parent=self.ledger)
        self.ledger.vat_type = TripletexVatType(self.client, parent=self.ledger)
        self.ledger.voucher = TripletexVoucher(self.client, parent=self.ledger)
        self.ledger.voucher.historical = TripletexVoucherHistorical(self.client, parent=self.ledger.voucher)
        self.ledger.voucher.opening_balance = TripletexVoucherOpeningBalance(self.client, parent=self.ledger.voucher)
