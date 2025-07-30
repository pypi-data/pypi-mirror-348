"""Data models specific to the Tripletex Account endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, IdUrl, TripletexResponse


class Account(BaseModel):
    """
    Represents a ledger account in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        number: Account number.
        number_pretty: Formatted account number.
        name: Account name.
        description: Account description.
        type: Account type (e.g., 'INCOME', 'EXPENSE').
        legal_vat_types: Allowed VAT types for this account.
        ledger_type: Type of ledger (e.g., 'GENERAL').
        balance_group: Balance group classification.
        vat_type: Default VAT type.
        vat_locked: Whether VAT type is locked.
        currency: Default currency.
        is_closeable: Can the account be closed?
        is_applicable_for_supplier_invoice: Usable for supplier invoices?
        require_reconciliation: Does the account require reconciliation?
        is_inactive: Is the account inactive?
        is_bank_account: Is it a bank account?
        is_invoice_account: Is it an invoice account?
        bank_account_number: Bank account number.
        bank_account_country: Bank account country.
        bank_name: Bank name.
        bank_account_iban: IBAN number.
        bank_account_swift: SWIFT/BIC code.
        saft_code: SAF-T code.
        grouping_code: Grouping code.
        display_name: User-friendly display name.
        requires_department: Does posting require a department?
        requires_project: Does posting require a project?
        invoicing_department: Default department for invoicing.
        is_postings_exist: Do postings exist for this account?
        quantity_type1: First quantity type.
        quantity_type2: Second quantity type.
        department: Associated department.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    number: Optional[int] = None
    number_pretty: Optional[str] = Field(None, alias="numberPretty")
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    legal_vat_types: Optional[List[IdUrl]] = Field(None, alias="legalVatTypes")
    ledger_type: Optional[str] = Field(None, alias="ledgerType")
    balance_group: Optional[str] = Field(None, alias="balanceGroup")
    vat_type: Optional[IdUrl] = Field(None, alias="vatType")
    vat_locked: Optional[bool] = Field(None, alias="vatLocked")
    currency: Optional[IdUrl] = None
    is_closeable: Optional[bool] = Field(None, alias="isCloseable")
    is_applicable_for_supplier_invoice: Optional[bool] = Field(None, alias="isApplicableForSupplierInvoice")
    require_reconciliation: Optional[bool] = Field(None, alias="requireReconciliation")
    is_inactive: Optional[bool] = Field(None, alias="isInactive")
    is_bank_account: Optional[bool] = Field(None, alias="isBankAccount")
    is_invoice_account: Optional[bool] = Field(None, alias="isInvoiceAccount")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    bank_account_country: Optional[IdUrl] = Field(None, alias="bankAccountCountry")
    bank_name: Optional[str] = Field(None, alias="bankName")
    bank_account_iban: Optional[str] = Field(None, alias="bankAccountIBAN")
    bank_account_swift: Optional[str] = Field(None, alias="bankAccountSWIFT")
    saft_code: Optional[str] = Field(None, alias="saftCode")
    grouping_code: Optional[str] = Field(None, alias="groupingCode")
    display_name: Optional[str] = Field(None, alias="displayName")
    requires_department: Optional[bool] = Field(None, alias="requiresDepartment")
    requires_project: Optional[bool] = Field(None, alias="requiresProject")
    invoicing_department: Optional[IdUrl] = Field(None, alias="invoicingDepartment")
    is_postings_exist: Optional[bool] = Field(None, alias="isPostingsExist")
    quantity_type1: Optional[IdUrl] = Field(None, alias="quantityType1")
    quantity_type2: Optional[IdUrl] = Field(None, alias="quantityType2")
    department: Optional[IdUrl] = None

    model_config = ConfigDict(populate_by_name=True)


class AccountCreate(BaseModel):
    """
    Model for creating a new ledger account.

    Contains required fields for account creation and optional fields
    that can be set during creation.
    """

    name: str
    number: int
    description: Optional[str] = None
    ledger_type: Optional[str] = Field(None, alias="ledgerType")
    vat_type: Optional[IdUrl] = Field(None, alias="vatType")
    vat_locked: Optional[bool] = Field(None, alias="vatLocked")
    currency: Optional[IdUrl] = None
    is_closeable: Optional[bool] = Field(None, alias="isCloseable")
    is_applicable_for_supplier_invoice: Optional[bool] = Field(None, alias="isApplicableForSupplierInvoice")
    require_reconciliation: Optional[bool] = Field(None, alias="requireReconciliation")
    is_inactive: Optional[bool] = Field(None, alias="isInactive")
    is_bank_account: Optional[bool] = Field(None, alias="isBankAccount")
    is_invoice_account: Optional[bool] = Field(None, alias="isInvoiceAccount")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    bank_account_country: Optional[IdUrl] = Field(None, alias="bankAccountCountry")
    bank_name: Optional[str] = Field(None, alias="bankName")
    bank_account_iban: Optional[str] = Field(None, alias="bankAccountIBAN")
    bank_account_swift: Optional[str] = Field(None, alias="bankAccountSWIFT")
    saft_code: Optional[str] = Field(None, alias="saftCode")
    grouping_code: Optional[str] = Field(None, alias="groupingCode")
    requires_department: Optional[bool] = Field(None, alias="requiresDepartment")
    requires_project: Optional[bool] = Field(None, alias="requiresProject")
    invoicing_department: Optional[IdUrl] = Field(None, alias="invoicingDepartment")
    quantity_type1: Optional[IdUrl] = Field(None, alias="quantityType1")
    quantity_type2: Optional[IdUrl] = Field(None, alias="quantityType2")
    department: Optional[IdUrl] = None

    model_config = ConfigDict(populate_by_name=True)


class AccountUpdate(BaseModel):
    """
    Model for updating an existing ledger account.

    All fields are optional since only fields that need to be changed
    are included in update requests.
    """

    name: Optional[str] = None
    number: Optional[int] = None
    description: Optional[str] = None
    ledger_type: Optional[str] = Field(None, alias="ledgerType")
    vat_type: Optional[IdUrl] = Field(None, alias="vatType")
    vat_locked: Optional[bool] = Field(None, alias="vatLocked")
    currency: Optional[IdUrl] = None
    is_closeable: Optional[bool] = Field(None, alias="isCloseable")
    is_applicable_for_supplier_invoice: Optional[bool] = Field(None, alias="isApplicableForSupplierInvoice")
    require_reconciliation: Optional[bool] = Field(None, alias="requireReconciliation")
    is_inactive: Optional[bool] = Field(None, alias="isInactive")
    is_bank_account: Optional[bool] = Field(None, alias="isBankAccount")
    is_invoice_account: Optional[bool] = Field(None, alias="isInvoiceAccount")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    bank_account_country: Optional[IdUrl] = Field(None, alias="bankAccountCountry")
    bank_name: Optional[str] = Field(None, alias="bankName")
    bank_account_iban: Optional[str] = Field(None, alias="bankAccountIBAN")
    bank_account_swift: Optional[str] = Field(None, alias="bankAccountSWIFT")
    saft_code: Optional[str] = Field(None, alias="saftCode")
    grouping_code: Optional[str] = Field(None, alias="groupingCode")
    requires_department: Optional[bool] = Field(None, alias="requiresDepartment")
    requires_project: Optional[bool] = Field(None, alias="requiresProject")
    invoicing_department: Optional[IdUrl] = Field(None, alias="invoicingDepartment")
    quantity_type1: Optional[IdUrl] = Field(None, alias="quantityType1")
    quantity_type2: Optional[IdUrl] = Field(None, alias="quantityType2")
    department: Optional[IdUrl] = None

    model_config = ConfigDict(populate_by_name=True)


class AccountResponse(TripletexResponse[Account]):
    """Response wrapper for a list of Account objects."""


class LedgerAccount(BaseModel):
    """
    Represents ledger account details including balances and postings.

    Attributes:
        account: The associated Account object.
        sum_amount: Sum of postings in base currency.
        currency: Currency used for sum_amount_currency.
        sum_amount_currency: Sum of postings in the specified currency.
        opening_balance: Opening balance in base currency.
        opening_balance_currency: Opening balance in the specified currency.
        closing_balance: Closing balance in base currency.
        closing_balance_currency: Closing balance in the specified currency.
        balance_out_in_account_currency: Balance out in account currency.
        postings: List of postings associated with this ledger account.
    """

    account: Optional[Account] = None
    sum_amount: Optional[float] = Field(None, alias="sumAmount")
    currency: Optional[IdUrl] = None
    sum_amount_currency: Optional[float] = Field(None, alias="sumAmountCurrency")
    opening_balance: Optional[float] = Field(None, alias="openingBalance")
    opening_balance_currency: Optional[float] = Field(None, alias="openingBalanceCurrency")
    closing_balance: Optional[float] = Field(None, alias="closingBalance")
    closing_balance_currency: Optional[float] = Field(None, alias="closingBalanceCurrency")
    balance_out_in_account_currency: Optional[float] = Field(None, alias="balanceOutInAccountCurrency")
    postings: Optional[List[IdUrl]] = None

    model_config = ConfigDict(populate_by_name=True)


class LedgerAccountResponse(TripletexResponse[LedgerAccount]):
    """Response wrapper for a list of LedgerAccount objects."""
