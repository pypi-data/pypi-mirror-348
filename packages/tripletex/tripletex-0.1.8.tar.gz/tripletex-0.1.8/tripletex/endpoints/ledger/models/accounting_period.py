"""Data models for Tripletex Accounting Period endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class AccountingPeriod(BaseModel):
    """
    Represents an accounting period (typically a month) in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        name: Period name (e.g., "January 2024").
        number: Period number (e.g., 1 for January).
        start: Start date of the period.
        end: End date of the period.
        is_closed: Is the period closed for postings?
        check_ledger_log_employee_name: Name of employee who checked the ledger log.
        check_ledger_log_employee_picture_id: Picture ID of employee who checked.
        check_ledger_log_time: Timestamp when the ledger log was checked.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    number: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None
    is_closed: Optional[bool] = Field(None, alias="isClosed")
    check_ledger_log_employee_name: Optional[str] = Field(None, alias="checkLedgerLogEmployeeName")
    check_ledger_log_employee_picture_id: Optional[int] = Field(None, alias="checkLedgerLogEmployeePictureId")
    check_ledger_log_time: Optional[str] = Field(None, alias="checkLedgerLogTime")

    model_config = ConfigDict(populate_by_name=True)


class AccountingPeriodResponse(TripletexResponse[AccountingPeriod]):
    """Response wrapper for a list of AccountingPeriod objects."""
