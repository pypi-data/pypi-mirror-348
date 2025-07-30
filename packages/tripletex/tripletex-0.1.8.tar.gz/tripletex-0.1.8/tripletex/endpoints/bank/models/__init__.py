from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import TripletexResponse

from .internal_match import (  # ReconciliationEntry, # Defined above, decide which one to use or rename; ReconciliationEntryDetail, # Defined above, decide which one to use or rename; ReconciliationEntryEntryType, # Defined above
    Change,
    ChangeChangeType,
    ContainerTagDivTag,
    ReconciliationGroup,
    ReconciliationMatch,
    ReconciliationMatchResponse,
)


class BankStatementFileFormatSupport(str):
    """Bank statement file formats supported by the bank."""

    CULTURA_BANK_TELEPAY = "CULTURA_BANK_TELEPAY"
    DANSKE_BANK_CSV = "DANSKE_BANK_CSV"
    DNB_CSV = "DNB_CSV"
    EIKA_TELEPAY = "EIKA_TELEPAY"
    HANDELSBANKEN_TELEPAY = "HANDELSBANKEN_TELEPAY"
    HAUGESUND_SPAREBANK_CSV = "HAUGESUND_SPAREBANK_CSV"
    LANDKREDITT_TELEPAY = "LANDKREDITT_TELEPAY"
    NORDEA_CSV = "NORDEA_CSV"
    SBANKEN_BEDRIFT_CSV = "SBANKEN_BEDRIFT_CSV"
    SBANKEN_PRIVAT_CSV = "SBANKEN_PRIVAT_CSV"
    SPAREBANK1_TELEPAY = "SPAREBANK1_TELEPAY"
    SPAREBANKEN_OST_TELEPAY = "SPAREBANKEN_OST_TELEPAY"
    SPAREBANKEN_SOR_TELEPAY = "SPAREBANKEN_SOR_TELEPAY"
    SPAREBANKEN_VEST_TELEPAY = "SPAREBANKEN_VEST_TELEPAY"
    TRANSFERWISE = "TRANSFERWISE"
    VISMA_ACCOUNT_STATEMENT = "VISMA_ACCOUNT_STATEMENT"
    VISMA_ACCOUNT_STATEMENT_PDS2_PLATFORM_AGNOSTIC = "VISMA_ACCOUNT_STATEMENT_PDS2_PLATFORM_AGNOSTIC"
    VISMA_ACCOUNT_STATEMENT_PLATFORM_AGNOSTIC = "VISMA_ACCOUNT_STATEMENT_PLATFORM_AGNOSTIC"
    VISMA_ACCOUNT_STATEMENT_PSD2 = "VISMA_ACCOUNT_STATEMENT_PSD2"
    ZTL = "ZTL"


class BankPlatform(str):
    """Bank platform."""

    INDEPENDENT = "INDEPENDENT"
    SDC = "SDC"
    TIETO_EVRY = "TIETO_EVRY"
    UNKNOWN = "UNKNOWN"


class AutoPaySupport(BaseModel):
    """Auto pay support information."""

    id: Optional[int] = None
    upload_needed: Optional[bool] = Field(None, alias="uploadNeeded")
    is_eika_type: Optional[bool] = Field(None, alias="isEikaType")
    has_org_number: Optional[bool] = Field(None, alias="hasOrgNumber")
    is_psd_2_type: Optional[bool] = Field(None, alias="isPsd2Type")
    has_approve_in_online_banking: Optional[bool] = Field(None, alias="hasApproveInOnlineBanking")
    required_bank_field_ids: Optional[List[int]] = Field(None, alias="requiredBankFieldIds")

    model_config = ConfigDict(populate_by_name=True)


class Bank(BaseModel):
    """Bank model representing a financial institution."""

    id: int
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    name: Optional[str] = None  # Bank name
    bank_statement_file_format_support: Optional[List[str]] = Field(None, alias="bankStatementFileFormatSupport")
    register_numbers: Optional[List[int]] = Field(None, alias="registerNumbers")
    display_name: Optional[str] = Field(None, alias="displayName")  # Bank name to comply with LoadableDropdown
    auto_pay_support: Optional[AutoPaySupport] = Field(None, alias="autoPaySupport")
    platform: Optional[str] = None  # Bank platform

    model_config = ConfigDict(populate_by_name=True)


class BankResponse(TripletexResponse[Bank]):
    """Response wrapper for a single Bank object."""


class Employee(BaseModel):
    """Employee model for bank transaction comment."""

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")

    model_config = ConfigDict(populate_by_name=True)


class BankTransactionComment(BaseModel):
    """Bank transaction comment model."""

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    comment: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    bank_transaction_id: Optional[int] = Field(None, alias="bankTransactionId")
    external_payment_id: Optional[str] = Field(None, alias="externalPaymentId")
    employee: Optional[Employee] = None
    actual_employee_id: Optional[int] = Field(None, alias="actualEmployeeId")
    actual_employee_company_id: Optional[int] = Field(None, alias="actualEmployeeCompanyId")
    actual_employee_name: Optional[str] = Field(None, alias="actualEmployeeName")

    model_config = ConfigDict(populate_by_name=True)


class BankTransactionCommentCreate(BaseModel):
    """Model for creating a bank transaction comment."""

    comment: str

    model_config = ConfigDict(populate_by_name=True)


class BankTransactionCommentResponse(TripletexResponse[BankTransactionComment]):
    """Response wrapper for a single BankTransactionComment object."""


# Bank Reconciliation Models
class Account(BaseModel):
    """Account model for bank reconciliation."""

    id: int
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    vat_type: Optional[dict] = Field(None, alias="vatType")
    currency: Optional[dict] = None
    is_inactive: Optional[bool] = Field(None, alias="isInactive")
    is_applicable_for_supplier_invoice: Optional[bool] = Field(None, alias="isApplicableForSupplierInvoice")
    is_applicable_for_customer_invoice: Optional[bool] = Field(None, alias="isApplicableForCustomerInvoice")
    is_applicable_for_project_invoice: Optional[bool] = Field(None, alias="isApplicableForProjectInvoice")
    ledger_account: Optional[dict] = Field(None, alias="ledgerAccount")
    customer_account: Optional[dict] = Field(None, alias="customerAccount")
    supplier_account: Optional[dict] = Field(None, alias="supplierAccount")
    employee_account: Optional[dict] = Field(None, alias="employeeAccount")
    project_account: Optional[dict] = Field(None, alias="projectAccount")
    product_account: Optional[dict] = Field(None, alias="productAccount")

    model_config = ConfigDict(populate_by_name=True)


class BankReconciliation(BaseModel):
    """Bank reconciliation model."""

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    account: Optional[Account] = None
    accounting_period: Optional[dict] = Field(None, alias="accountingPeriod")
    from_date: Optional[date] = Field(None, alias="fromDate")
    to_date: Optional[date] = Field(None, alias="toDate")
    is_closed: Optional[bool] = Field(None, alias="isClosed")
    closed_date: Optional[date] = Field(None, alias="closedDate")
    closed_by_contact: Optional[dict] = Field(None, alias="closedByContact")
    opening_balance: Optional[float] = Field(None, alias="openingBalance")
    closing_balance: Optional[float] = Field(None, alias="closingBalance")
    account_balance: Optional[float] = Field(None, alias="accountBalance")
    adjustment_amount: Optional[float] = Field(None, alias="adjustmentAmount")
    is_adjustment_open: Optional[bool] = Field(None, alias="isAdjustmentOpen")
    has_unmatched_transactions: Optional[bool] = Field(None, alias="hasUnmatchedTransactions")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class BankReconciliationCreate(BaseModel):
    """Model for creating a bank reconciliation."""

    account: Dict[str, Any]
    accountingPeriod: Dict[str, Any]  # noqa - Pydantic V1 style for compatibility
    type: str  # Required field from swagger spec

    model_config = ConfigDict(populate_by_name=True)


class BankReconciliationUpdate(BaseModel):
    """Model for updating a bank reconciliation."""

    account: Dict[str, Any]
    accountingPeriod: Dict[str, Any]  # noqa - Pydantic V1 style for compatibility
    type: str

    model_config = ConfigDict(populate_by_name=True)


class BankReconciliationResponse(TripletexResponse[BankReconciliation]):
    """Response wrapper for a single BankReconciliation object."""

    # Override the value property to handle None values
    _value: Optional[BankReconciliation] = None  # Ensure _value is defined

    @property
    def value(self) -> Optional[BankReconciliation]:
        """Get the value, which can be None."""
        return self._value

    @value.setter
    def value(self, value: Optional[BankReconciliation]) -> None:
        """Set the value, allowing None."""
        self._value = value


class BankReconciliationAdjustment(BaseModel):
    """Model for bank reconciliation adjustment."""

    adjustment_amount: float = Field(..., alias="adjustmentAmount")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class UnmatchedTransactionsCsv(BaseModel):
    """Model for unmatched transactions CSV."""

    file_format: str = Field(..., alias="fileFormat")

    model_config = ConfigDict(populate_by_name=True)


# Bank Reconciliation Entry Models
class BankReconciliationEntryBankTransaction(BaseModel):
    """Model for bank reconciliation entry bank transaction."""

    bank_transaction_ids: List[int] = Field(..., alias="bankTransactionIds")
    reconciliation_id: int = Field(..., alias="reconciliationId")

    model_config = ConfigDict(populate_by_name=True)


class BankReconciliationEntryBankTransactionResponse(TripletexResponse[BankReconciliationEntryBankTransaction]):
    """Response wrapper for a bank reconciliation entry bank transaction."""


class ReconciliationEntryEntryType(str):  # Note: This is also in internal_match.py. Ensure consistency or one source.
    """Entry type for reconciliation entry."""

    POSTING = "Posting"
    BANK_TRANSACTION = "BankTransaction"


class ReconciliationEntryDetail(BaseModel):  # Note: This is also in internal_match.py. Ensure consistency or one source.
    """Detail for reconciliation entry."""

    description: Optional[str] = None  # internal_match.py has key, value, value_for_pdf
    amount_currency: Optional[float] = Field(None, alias="amountCurrency")

    model_config = ConfigDict(populate_by_name=True)


class ReconciliationEntry(BaseModel):  # Note: This is also in internal_match.py. Ensure consistency or one source.
    """Model for reconciliation entry."""

    id: Optional[int] = None
    entry_type: Optional[ReconciliationEntryEntryType] = Field(None, alias="entryType")
    amount_currency: Optional[float] = Field(None, alias="amountCurrency")
    details_list: Optional[List[ReconciliationEntryDetail]] = Field(None, alias="detailsList")
    date: Optional[str] = None
    voucher_id: Optional[int] = Field(None, alias="voucherId")
    is_query_match: Optional[bool] = Field(None, alias="isQueryMatch")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class ListResponseReconciliationEntry(TripletexResponse[List[ReconciliationEntry]]):
    """Response wrapper for a list of reconciliation entries."""


# Bank Statement Models
class BankTransaction(BaseModel):
    """Bank transaction model."""

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    amount: Optional[float] = None
    amount_currency: Optional[float] = Field(None, alias="amountCurrency")
    currency_rate: Optional[float] = Field(None, alias="currencyRate")
    interest_date: Optional[str] = Field(None, alias="interestDate")
    transaction_date: Optional[str] = Field(None, alias="transactionDate")
    description: Optional[str] = None
    kid: Optional[str] = None
    reference: Optional[str] = None
    type: Optional[str] = None
    is_reconciled: Optional[bool] = Field(None, alias="isReconciled")
    bank_statement_id: Optional[int] = Field(None, alias="bankStatementId")

    model_config = ConfigDict(populate_by_name=True)


class BankTransactionCreate(BaseModel):  # Added for test setup
    amount_currency: float = Field(alias="amountCurrency")
    transaction_date: str = Field(alias="transactionDate")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class BankTransactionResponse(TripletexResponse[BankTransaction]):
    """Response wrapper for a list of BankTransaction objects."""


class BankStatement(BaseModel):
    """Bank statement model."""

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[dict]] = None
    url: Optional[str] = None
    opening_balance_currency: Optional[float] = Field(None, alias="openingBalanceCurrency")
    closing_balance_currency: Optional[float] = Field(None, alias="closingBalanceCurrency")
    file_name: Optional[str] = Field(None, alias="fileName")
    bank: Optional[Bank] = None
    from_date: Optional[str] = Field(None, alias="fromDate")
    to_date: Optional[str] = Field(None, alias="toDate")
    transactions: Optional[List[BankTransaction]] = None

    model_config = ConfigDict(populate_by_name=True)


class BankStatementCreate(BaseModel):  # Added for test setup
    bank_account_id: int = Field(alias="bankAccountId")
    transactions: List[BankTransactionCreate]

    model_config = ConfigDict(populate_by_name=True)


class BankStatementResponse(TripletexResponse[BankStatement]):
    """Response wrapper for a single BankStatement object."""


class BankStatementImportFileFormat(str):  # Note: This is duplicated (BankStatementFileFormatSupport)
    """Bank statement file formats supported by the bank."""

    CULTURA_BANK_TELEPAY = "CULTURA_BANK_TELEPAY"
    DANSKE_BANK_CSV = "DANSKE_BANK_CSV"
    DNB_CSV = "DNB_CSV"
    EIKA_TELEPAY = "EIKA_TELEPAY"
    HANDELSBANKEN_TELEPAY = "HANDELSBANKEN_TELEPAY"
    HAUGESUND_SPAREBANK_CSV = "HAUGESUND_SPAREBANK_CSV"
    LANDKREDITT_TELEPAY = "LANDKREDITT_TELEPAY"
    NORDEA_CSV = "NORDEA_CSV"
    SBANKEN_BEDRIFT_CSV = "SBANKEN_BEDRIFT_CSV"
    SBANKEN_PRIVAT_CSV = "SBANKEN_PRIVAT_CSV"
    SPAREBANK1_TELEPAY = "SPAREBANK1_TELEPAY"
    SPAREBANKEN_OST_TELEPAY = "SPAREBANKEN_OST_TELEPAY"
    SPAREBANKEN_SOR_TELEPAY = "SPAREBANKEN_SOR_TELEPAY"
    SPAREBANKEN_VEST_TELEPAY = "SPAREBANKEN_VEST_TELEPAY"
    TRANSFERWISE = "TRANSFERWISE"
    VISMA_ACCOUNT_STATEMENT = "VISMA_ACCOUNT_STATEMENT"
    VISMA_ACCOUNT_STATEMENT_PDS2_PLATFORM_AGNOSTIC = "VISMA_ACCOUNT_STATEMENT_PDS2_PLATFORM_AGNOSTIC"
    VISMA_ACCOUNT_STATEMENT_PLATFORM_AGNOSTIC = "VISMA_ACCOUNT_STATEMENT_PLATFORM_AGNOSTIC"
    VISMA_ACCOUNT_STATEMENT_PSD2 = "VISMA_ACCOUNT_STATEMENT_PSD2"
    ZTL = "ZTL"


class BankStatementImport(BaseModel):
    """Model for importing a bank statement."""

    file: Any  # Using Any for File type
    bankId: int
    accountId: int
    fromDate: str
    toDate: str
    externalId: Optional[str] = None
    fileFormat: str

    model_config = ConfigDict(populate_by_name=True)


# Make internal_match models available under this namespace

# To avoid name clashes for ReconciliationEntry, ReconciliationEntryDetail, ReconciliationEntryEntryType
# from internal_match.py, they are commented out here.
# The crud/internal_match.py should import them directly from .internal_match
# All other files that need the "general" versions will get them from this __init__.py

# For clarity, let's explicitly list what is available from this __init__
__all__ = [
    "BankStatementFileFormatSupport",
    "BankPlatform",
    "AutoPaySupport",
    "Bank",
    "BankResponse",
    "Employee",
    "BankTransactionComment",
    "BankTransactionCommentCreate",
    "BankTransactionCommentResponse",
    "Account",
    "BankReconciliation",
    "BankReconciliationCreate",
    "BankReconciliationUpdate",
    "BankReconciliationResponse",
    "BankReconciliationAdjustment",
    "UnmatchedTransactionsCsv",
    "BankReconciliationEntryBankTransaction",
    "BankReconciliationEntryBankTransactionResponse",
    "ReconciliationEntryEntryType",  # General version
    "ReconciliationEntryDetail",  # General version
    "ReconciliationEntry",  # General version
    "ListResponseReconciliationEntry",
    "BankTransaction",
    "BankTransactionCreate",
    "BankTransactionResponse",
    "BankStatement",
    "BankStatementCreate",
    "BankStatementResponse",
    "BankStatementImportFileFormat",
    "BankStatementImport",
    # From internal_match - carefully selected to avoid re-definition issues
    "Change",
    "ChangeChangeType",
    "ContainerTagDivTag",
    "ReconciliationGroup",  # Specific to internal_match context
    "ReconciliationMatch",  # Specific to internal_match context
    "ReconciliationMatchResponse",  # Specific to internal_match context
]
