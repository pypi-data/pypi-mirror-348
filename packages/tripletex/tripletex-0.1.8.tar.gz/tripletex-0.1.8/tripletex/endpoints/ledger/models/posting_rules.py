"""Data models specific to the Tripletex Ledger Posting Rules endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, IdUrl


class PostingRules(BaseModel):
    """
    Represents the posting rules configuration in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        account_receivable_customers_id: Default accounts receivable account.
        account_debt_vendors_id: Default accounts payable account (vendors).
        account_debt_employees_and_owners_id: Default debt account (employees/owners).
        account_round_diff_id: Account for rounding differences.
        vat_per_department: Is VAT tracked per department?
        multiple_industries: Does the company operate in multiple industries?
        default_business_activity_type_id: Default business activity type ID.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    account_receivable_customers_id: Optional[IdUrl] = Field(None, alias="accountReceivableCustomersId")
    account_debt_vendors_id: Optional[IdUrl] = Field(None, alias="accountDebtVendorsId")
    account_debt_employees_and_owners_id: Optional[IdUrl] = Field(None, alias="accountDebtEmployeesAndOwnersId")
    account_round_diff_id: Optional[IdUrl] = Field(None, alias="accountRoundDiffId")
    vat_per_department: Optional[bool] = Field(None, alias="vatPerDepartment")
    multiple_industries: Optional[bool] = Field(None, alias="multipleIndustries")
    default_business_activity_type_id: Optional[int] = Field(None, alias="defaultBusinessActivityTypeId")

    model_config = ConfigDict(populate_by_name=True)


class PostingRulesResponse(BaseModel):
    """Response wrapper for a single PostingRules object."""

    value: Optional[PostingRules] = None

    model_config = ConfigDict(populate_by_name=True)
