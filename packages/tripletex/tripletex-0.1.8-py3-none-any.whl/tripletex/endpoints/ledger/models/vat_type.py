"""Data models for VAT types in Tripletex."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class VatType(BaseModel):
    """
    Represents a VAT type in Tripletex.

    Attributes:
        id: Unique identifier.
        version: Version number.
        changes: List of changes.
        url: Resource URL.
        name: VAT type name.
        number: VAT type number.
        percentage: VAT percentage.
        vat_return_type: Type of VAT return.
        display_name: User-friendly display name.
        deduction_percentage: Percentage of deduction allowed for this VAT type.
    """

    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    percentage: Optional[float] = None
    vat_return_type: Optional[str] = Field(None, alias="vatReturnType")
    display_name: Optional[str] = Field(None, alias="displayName")
    deduction_percentage: Optional[float] = Field(None, alias="deductionPercentage")

    model_config = ConfigDict(populate_by_name=True)


class CreateRelativeVatTypeRequest(BaseModel):
    """
    Request model for creating a relative VAT type.

    Attributes:
        name: VAT type name, max 8 characters.
        vat_type_id: VAT type ID. The relative VAT type will behave like this VAT type,
                    except for the basis for calculating the VAT deduction.
        percentage: Basis percentage. This percentage will be multiplied with the transaction
                   amount to find the amount that will be the basis for calculating the deduction amount.
    """

    name: str = Field(..., description="VAT type name, max 8 characters")
    vat_type_id: int = Field(..., alias="vatTypeId", description="VAT type ID")
    percentage: float = Field(..., description="Basis percentage")

    model_config = ConfigDict(populate_by_name=True)


class VatTypeResponse(TripletexResponse[VatType]):
    """Response wrapper for a list of VatType objects."""
