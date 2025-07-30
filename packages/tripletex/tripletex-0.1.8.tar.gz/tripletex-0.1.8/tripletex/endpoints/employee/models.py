# /workspace/tripletex/endpoints/employee/models.py
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import IdUrl, TripletexResponse


class Employee(BaseModel):
    """Represents a Tripletex employee."""

    first_name: Optional[str] = None
    """Employee's first name."""
    last_name: Optional[str] = None
    """Employee's last name."""
    id: Optional[int] = None
    """Unique identifier."""
    version: Optional[int] = None
    """Version number for optimistic locking."""
    changes: Optional[list[str]] = None
    """List of changes."""
    url: Optional[str] = None
    """URL to the employee resource."""
    display_name: Optional[str] = None
    """Full name for display."""
    employee_number: Optional[str] = None
    """Employee identification number."""
    date_of_birth: Optional[str] = None
    """Date of birth (YYYY-MM-DD)."""
    email: Optional[str] = None
    """Email address."""
    phone_number_mobile_country: Optional[IdUrl] = None
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str] = None
    """Mobile phone number."""
    phone_number_home: Optional[str] = None
    """Home phone number."""
    phone_number_work: Optional[str] = None
    """Work phone number."""
    national_identity_number: Optional[str] = None
    """National identity number."""
    dnumber: Optional[str] = None
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl] = None
    """International ID details."""
    bank_account_number: Optional[str] = None
    """Bank account number."""
    iban: Optional[str] = None
    """IBAN number."""
    bic: Optional[str] = None
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int] = None
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool] = None
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl] = None
    """Type of user."""
    allow_information_registration: Optional[bool] = None
    """Flag allowing information registration."""
    is_contact: Optional[bool] = None
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool] = None
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str] = None
    """Additional comments."""
    address: Optional[IdUrl] = None
    """Link to the employee's address."""
    department: IdUrl
    """Link to the employee's department."""
    employments: Optional[List[IdUrl]] = None
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl] = None
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl] = None
    """Link to the employee category."""
    is_auth_project_overview_url: Optional[bool] = None
    """Flag related to project overview authorization."""
    picture_id: Optional[int] = None
    """ID of the employee's picture."""
    company_id: Optional[int] = None
    """ID of the associated company."""

    model_config = ConfigDict(populate_by_name=True)


class EmployeeCreate(BaseModel):
    """Input model for creating an Employee."""

    first_name: str = Field(..., alias="firstName")
    """Employee's first name (required)."""
    last_name: str = Field(..., alias="lastName")
    """Employee's last name (required)."""
    email: str
    """Email address (required)."""
    department: IdUrl
    """Link to the employee's department (required)."""
    employee_number: Optional[str] = Field(None, alias="employeeNumber")
    """Employee identification number."""
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    """Date of birth (YYYY-MM-DD)."""
    phone_number_mobile_country: Optional[IdUrl] = Field(None, alias="phoneNumberMobileCountry")
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str] = Field(None, alias="phoneNumberMobile")
    """Mobile phone number."""
    phone_number_home: Optional[str] = Field(None, alias="phoneNumberHome")
    """Home phone number."""
    phone_number_work: Optional[str] = Field(None, alias="phoneNumberWork")
    """Work phone number."""
    national_identity_number: Optional[str] = Field(None, alias="nationalIdentityNumber")
    """National identity number."""
    dnumber: Optional[str] = None
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl] = Field(None, alias="internationalId")
    """International ID details."""
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    """Bank account number."""
    iban: Optional[str] = None
    """IBAN number."""
    bic: Optional[str] = None
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int] = Field(None, alias="creditorBankCountryId")
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool] = Field(None, alias="usesAbroadPayment")
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl] = Field(None, alias="userType")
    """Type of user."""
    allow_information_registration: Optional[bool] = Field(None, alias="allowInformationRegistration")
    """Flag allowing information registration."""
    is_contact: Optional[bool] = Field(None, alias="isContact")
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool] = Field(None, alias="isProxy")
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str] = None
    """Additional comments."""
    address: Optional[IdUrl] = None
    """Link to the employee's address."""
    employments: Optional[List[IdUrl]] = None
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl] = Field(None, alias="holidayAllowanceEarned")
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl] = Field(None, alias="employeeCategory")
    """Link to the employee category."""
    # is_auth_project_overview_url: Optional[bool] = Field(None, alias="isAuthProjectOverviewUrl") # Removed: API rejects this field on create/update
    picture_id: Optional[int] = Field(None, alias="pictureId")
    """ID of the employee's picture."""

    model_config = ConfigDict(populate_by_name=True)  # Use alias for population


class EmployeeUpdate(BaseModel):
    """Input model for updating an Employee. All fields are optional."""

    first_name: Optional[str] = Field(None, alias="firstName")
    """Employee's first name."""
    last_name: Optional[str] = Field(None, alias="lastName")
    """Employee's last name."""
    email: Optional[str] = None
    """Email address."""
    department: Optional[IdUrl] = None
    """Link to the employee's department."""
    employee_number: Optional[str] = Field(None, alias="employeeNumber")
    """Employee identification number."""
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    """Date of birth (YYYY-MM-DD)."""
    phone_number_mobile_country: Optional[IdUrl] = Field(None, alias="phoneNumberMobileCountry")
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str] = Field(None, alias="phoneNumberMobile")
    """Mobile phone number."""
    phone_number_home: Optional[str] = Field(None, alias="phoneNumberHome")
    """Home phone number."""
    phone_number_work: Optional[str] = Field(None, alias="phoneNumberWork")
    """Work phone number."""
    national_identity_number: Optional[str] = Field(None, alias="nationalIdentityNumber")
    """National identity number."""
    dnumber: Optional[str] = None
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl] = Field(None, alias="internationalId")
    """International ID details."""
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    """Bank account number."""
    iban: Optional[str] = None
    """IBAN number."""
    bic: Optional[str] = None
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int] = Field(None, alias="creditorBankCountryId")
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool] = Field(None, alias="usesAbroadPayment")
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl] = Field(None, alias="userType")
    """Type of user."""
    allow_information_registration: Optional[bool] = Field(None, alias="allowInformationRegistration")
    """Flag allowing information registration."""
    is_contact: Optional[bool] = Field(None, alias="isContact")
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool] = Field(None, alias="isProxy")
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str] = None
    """Additional comments."""
    address: Optional[IdUrl] = None
    """Link to the employee's address."""
    employments: Optional[List[IdUrl]] = None
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl] = Field(None, alias="holidayAllowanceEarned")
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl] = Field(None, alias="employeeCategory")
    """Link to the employee category."""
    # is_auth_project_overview_url: Optional[bool] = Field(None, alias="isAuthProjectOverviewUrl") # Removed: API rejects this field on create/update
    picture_id: Optional[int] = Field(None, alias="pictureId")
    """ID of the employee's picture."""

    model_config = ConfigDict(populate_by_name=True)  # Use alias for population


class EmployeeResponse(TripletexResponse[Employee]):
    """Response wrapper for a list of Employee objects."""
