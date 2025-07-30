from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import TripletexResponse


class ChangeChangeType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    DO_NOT_SHOW = "DO_NOT_SHOW"
    LOCKED = "LOCKED"
    REOPENED = "REOPENED"
    UPDATE = "UPDATE"


class Change(BaseModel):
    employee_id: Optional[int] = Field(None, alias="employeeId")
    timestamp: Optional[str] = None
    change_type: Optional[ChangeChangeType] = Field(None, alias="changeType")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class ReconciliationEntryEntryType(str, Enum):
    BANK_TRANSACTION = "BankTransaction"
    POSTING = "Posting"


class ContainerTagDivTag(BaseModel):
    tag_name: Optional[str] = Field(None, alias="tagName")
    num_children: Optional[int] = Field(None, alias="numChildren")

    model_config = ConfigDict(populate_by_name=True)


class ReconciliationEntryDetail(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    value_for_pdf: Optional[ContainerTagDivTag] = Field(None, alias="valueForPDF")

    model_config = ConfigDict(populate_by_name=True)


class ReconciliationEntry(BaseModel):
    id: Optional[int] = None
    entry_type: Optional[ReconciliationEntryEntryType] = Field(None, alias="entryType")
    amount_currency: Optional[float] = Field(None, alias="amountCurrency")
    details_list: Optional[List[ReconciliationEntryDetail]] = Field(None, alias="detailsList")
    date: Optional[str] = None
    voucher_id: Optional[int] = Field(None, alias="voucherId")
    is_query_match: Optional[bool] = Field(None, alias="isQueryMatch")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class ReconciliationGroup(BaseModel):
    title: Optional[str] = None
    total_amount: Optional[float] = Field(None, alias="totalAmount")
    entries: Optional[List[ReconciliationEntry]] = None

    model_config = ConfigDict(populate_by_name=True)


class ReconciliationMatch(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    reconciliation_id: Optional[int] = Field(None, alias="reconciliationId")
    is_approved: Optional[bool] = Field(None, alias="isApproved")
    postings_group: Optional[ReconciliationGroup] = Field(None, alias="postingsGroup")
    transactions_group: Optional[ReconciliationGroup] = Field(None, alias="transactionsGroup")

    model_config = ConfigDict(populate_by_name=True)


class ReconciliationMatchResponse(TripletexResponse[ReconciliationMatch]):
    pass
