"""Data models specific to the Tripletex Voucher endpoints."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError

from tripletex.core.models import Change, IdRef, IdUrl, TripletexResponse

# Import the consolidated PostingCreate model and Posting model
from .posting import Posting, PostingCreate

# Import GBAT10 models from the dedicated file


class Voucher(BaseModel):
    """
    Represents a voucher (journal entry) in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        date: Voucher date.
        number: Voucher number.
        temp_number: Temporary number before finalization.
        year: Fiscal year.
        description: Voucher description.
        voucher_type: Associated voucher type.
        reverse_voucher: Link to the reversing voucher, if any.
        postings: List of postings (lines) in the voucher.
        document: Associated document.
        attachment: Associated attachment.
        external_voucher_number: External reference number.
        edi_document: Associated EDI document.
        supplier_voucher_type: Type specific to supplier vouchers.
        was_auto_matched: Was the voucher automatically matched?
        vendor_invoice_number: Vendor's invoice number.
        display_name: User-friendly display name.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    date: Optional[str] = None
    number: Optional[int] = None
    temp_number: Optional[int] = Field(None, alias="tempNumber")
    year: Optional[int] = None
    description: Optional[str] = None
    voucher_type: Optional[IdUrl] = Field(None, alias="voucherType")
    reverse_voucher: Optional[IdUrl] = Field(None, alias="reverseVoucher")
    postings: Optional[List[Posting]] = None
    document: Optional[IdUrl] = None
    attachment: Optional[IdUrl] = None
    external_voucher_number: Optional[str] = Field(None, alias="externalVoucherNumber")
    edi_document: Optional[IdUrl] = Field(None, alias="ediDocument")
    supplier_voucher_type: Optional[str] = Field(None, alias="supplierVoucherType")
    was_auto_matched: Optional[bool] = Field(None, alias="wasAutoMatched")
    vendor_invoice_number: Optional[str] = Field(None, alias="vendorInvoiceNumber")
    display_name: Optional[str] = Field(None, alias="displayName")

    model_config = ConfigDict(populate_by_name=True)


class VoucherCreate(BaseModel):
    """
    Model for creating a new voucher.

    Contains required fields for voucher creation and optional fields
    that can be set during creation.
    """

    date: str
    description: Optional[str] = None
    voucher_type: IdRef = Field(..., alias="voucherType")
    postings: List[PostingCreate]  # Postings are required for a valid voucher
    document: Optional[IdRef] = None
    attachment: Optional[IdRef] = None
    external_voucher_number: Optional[str] = Field(None, alias="externalVoucherNumber")
    supplier_voucher_type: Optional[str] = Field(None, alias="supplierVoucherType")
    vendor_invoice_number: Optional[str] = Field(None, alias="vendorInvoiceNumber")
    # Note: sendToLedger is a query parameter, not a field in the request body

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def check_voucher_balance_and_rows(self) -> "VoucherCreate":
        """Validate that postings exist, balance to zero, and have unique rows."""
        if not self.postings:
            raise PydanticCustomError(
                "value_error",
                "Voucher must have at least one posting.",
                {"postings": self.postings},
            )

        # Check balance (allow for small floating point inaccuracies)
        total_amount = sum(p.amount for p in self.postings)
        if abs(total_amount) > 1e-9:  # Using a small tolerance
            raise PydanticCustomError(
                "value_error",
                f"Voucher postings do not balance. Sum of amounts is {total_amount:.2f}, expected 0.",
                {"total_amount": total_amount},
            )

        # Check row uniqueness and > 0 (gt=0 check is done by PostingCreate)
        seen_rows = set()
        for posting in self.postings:
            if posting.row in seen_rows:
                raise PydanticCustomError(
                    "value_error",
                    f"Duplicate row number {posting.row} found in postings.",
                    {"row": posting.row},
                )
            seen_rows.add(posting.row)

        return self

    @field_validator("postings")
    @classmethod
    def check_at_least_two_postings_for_balance(cls, v: List[PostingCreate]) -> List[PostingCreate]:
        """Ensure there are at least two postings if balance is required."""
        # While technically a single posting of 0 could balance,
        # a real voucher typically needs at least two lines.
        if len(v) < 2:
            raise PydanticCustomError(
                "value_error",
                "Voucher must have at least two postings to balance.",
                {"num_postings": len(v)},
            )
        return v


class VoucherUpdate(BaseModel):
    """
    Model for updating an existing voucher.

    All fields are optional since only fields that need to be changed
    are included in update requests.
    """

    date: Optional[str] = None
    description: Optional[str] = None
    voucher_type: Optional[IdRef] = Field(None, alias="voucherType")
    postings: Optional[List[PostingCreate]] = None
    document: Optional[IdRef] = None
    attachment: Optional[IdRef] = None
    external_voucher_number: Optional[str] = Field(None, alias="externalVoucherNumber")
    supplier_voucher_type: Optional[str] = Field(None, alias="supplierVoucherType")
    vendor_invoice_number: Optional[str] = Field(None, alias="vendorInvoiceNumber")

    model_config = ConfigDict(populate_by_name=True)


class VoucherResponse(TripletexResponse[Voucher]):
    """Response wrapper for a list of Voucher objects."""


class VoucherHistorical(Voucher):
    """
    Represents a historical voucher in Tripletex.

    This model extends the standard Voucher model to represent historical voucher data.
    It inherits all attributes from the Voucher model.
    """


class VoucherHistoricalResponse(TripletexResponse[VoucherHistorical]):
    """Response wrapper for a list of VoucherHistorical objects."""


class VoucherOpeningBalance(Voucher):
    """
    Represents an opening balance voucher in Tripletex.

    This model extends the standard Voucher model to represent opening balance voucher data.
    It inherits all attributes from the Voucher model.
    """


class VoucherOpeningBalanceResponse(BaseModel):
    """
    Response wrapper for a single VoucherOpeningBalance object.

    The opening balance endpoint returns a different response structure
    compared to standard list endpoints, with a single 'value' field
    instead of 'values' and 'count'.
    """

    value: Optional[VoucherOpeningBalance] = None

    model_config = ConfigDict(populate_by_name=True)
