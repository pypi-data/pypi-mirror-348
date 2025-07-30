# -*- coding: utf-8 -*-
import datetime
import enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field

from tripletex.core.models import Change as CoreChange
from tripletex.core.models import IdUrl  # Added IdUrl import
from tripletex.core.models import TripletexResponse


class CompanyType(enum.Enum):

    NONE = "NONE"
    ENK = "ENK"
    AS = "AS"
    NUF = "NUF"
    ANS = "ANS"
    DA = "DA"
    PRE = "PRE"
    KS = "KS"
    ASA = "ASA"
    BBL = "BBL"
    BRL = "BRL"
    GFS = "GFS"
    SPA = "SPA"
    SF = "SF"
    IKS = "IKS"
    KF_FKF = "KF_FKF"
    FCD = "FCD"
    EOFG = "EOFG"
    BA = "BA"
    STI = "STI"
    ORG = "ORG"
    ESEK = "ESEK"
    SA = "SA"
    SAM = "SAM"
    BO = "BO"
    VPFO = "VPFO"
    OS = "OS"
    FLI = "FLI"
    Other = "Other"


class CompanyMigration(enum.Enum):

    NONE = "NONE"
    AGRO = "AGRO"


class Country(BaseModel):

    id: Optional[int] = Field(alias="id", default=None)
    version: Optional[int] = Field(alias="version", default=None)
    changes: Optional[List[CoreChange]] = Field(alias="changes", default=None)
    url: Optional[str] = Field(alias="url", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    displayName: Optional[str] = Field(alias="displayName", default=None)
    isoAlpha2Code: Optional[str] = Field(alias="isoAlpha2Code", default=None)
    isoAlpha3Code: Optional[str] = Field(alias="isoAlpha3Code", default=None)
    isoNumericCode: Optional[str] = Field(alias="isoNumericCode", default=None)


class Address(BaseModel):

    id: Optional[int] = Field(alias="id", default=None)
    version: Optional[int] = Field(alias="version", default=None)
    changes: Optional[List[CoreChange]] = Field(alias="changes", default=None)
    url: Optional[str] = Field(alias="url", default=None)
    addressLine1: Optional[str] = Field(alias="addressLine1", default=None)
    addressLine2: Optional[str] = Field(alias="addressLine2", default=None)
    postalCode: Optional[str] = Field(alias="postalCode", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    country: Optional[Country] = Field(alias="country", default=None)
    displayName: Optional[str] = Field(alias="displayName", default=None)
    addressAsString: Optional[str] = Field(alias="addressAsString", default=None)
    displayNameInklMatrikkel: Optional[str] = Field(alias="displayNameInklMatrikkel", default=None)
    knr: Optional[int] = Field(alias="knr", default=None)
    gnr: Optional[int] = Field(alias="gnr", default=None)
    bnr: Optional[int] = Field(alias="bnr", default=None)
    fnr: Optional[int] = Field(alias="fnr", default=None)
    snr: Optional[int] = Field(alias="snr", default=None)
    unitNumber: Optional[str] = Field(alias="unitNumber", default=None)


class Currency(BaseModel):

    id: Optional[int] = Field(alias="id", default=None)
    version: Optional[int] = Field(alias="version", default=None)
    changes: Optional[List[CoreChange]] = Field(alias="changes", default=None)
    url: Optional[str] = Field(alias="url", default=None)
    code: Optional[str] = Field(alias="code", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    factor: Optional[int] = Field(alias="factor", default=None)
    displayName: Optional[str] = Field(alias="displayName", default=None)
    isDisabled: Optional[bool] = Field(alias="isDisabled", default=None)


class Company(BaseModel):

    id: Optional[int] = Field(alias="id", default=None)
    version: Optional[int] = Field(alias="version", default=None)
    changes: Optional[List[CoreChange]] = Field(alias="changes", default=None)
    url: Optional[str] = Field(alias="url", default=None)
    name: str = Field(alias="name")
    displayName: Optional[str] = Field(alias="displayName", default=None)
    startDate: Optional[datetime.date] = Field(alias="startDate", default=None)
    endDate: Optional[datetime.date] = Field(alias="endDate", default=None)
    organizationNumber: Optional[str] = Field(alias="organizationNumber", default=None)
    # Modified to handle empty strings by using Union[EmailStr, str] and a validator
    email: Optional[Union[EmailStr, str]] = Field(alias="email", default=None)
    phoneNumber: Optional[str] = Field(alias="phoneNumber", default=None)
    phoneNumberMobile: Optional[str] = Field(alias="phoneNumberMobile", default=None)
    faxNumber: Optional[str] = Field(alias="faxNumber", default=None)
    address: Optional[Address] = Field(alias="address", default=None)
    company_type: Optional[CompanyType] = Field(alias="type", default=None)  # Renamed from 'type'
    currency: Optional[Currency] = Field(alias="currency", default=None)
    accountantOrSimilar: Optional[bool] = Field(alias="accountantOrSimilar", default=None)
    companyMigration: Optional[CompanyMigration] = Field(alias="companyMigration", default=None)
    invoiceShowDeliveryDate: Optional[bool] = Field(alias="invoiceShowDeliveryDate", default=None)
    postal_address: Optional[IdUrl] = Field(default=None, alias="postalAddress")
    physical_address: Optional[IdUrl] = Field(default=None, alias="physicalAddress")

    # Add a validator to handle empty email strings
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, dict) and "email" in obj and obj["email"] == "":
            obj["email"] = None
        return super().model_validate(obj, *args, **kwargs)


class Client(BaseModel):

    id: Optional[int] = Field(alias="id", default=None)
    version: Optional[int] = Field(alias="version", default=None)
    changes: Optional[List[CoreChange]] = Field(alias="changes", default=None)
    url: Optional[str] = Field(alias="url", default=None)
    name: str = Field(alias="name")
    displayName: Optional[str] = Field(alias="displayName", default=None)
    startDate: Optional[datetime.date] = Field(alias="startDate", default=None)
    endDate: Optional[datetime.date] = Field(alias="endDate", default=None)
    organizationNumber: Optional[str] = Field(alias="organizationNumber", default=None)
    # Modified to handle empty strings by using Union[EmailStr, str] and a validator
    email: Optional[Union[EmailStr, str]] = Field(alias="email", default=None)
    phoneNumber: Optional[str] = Field(alias="phoneNumber", default=None)
    phoneNumberMobile: Optional[str] = Field(alias="phoneNumberMobile", default=None)
    faxNumber: Optional[str] = Field(alias="faxNumber", default=None)
    address: Address = Field(alias="address")  # Assuming Client model might need similar review later if errors occur
    company_type: CompanyType = Field(alias="type")  # Renamed from 'type'
    currency: Optional[Currency] = Field(alias="currency", default=None)
    accountantOrSimilar: Optional[bool] = Field(alias="accountantOrSimilar", default=None)
    companyMigration: Optional[CompanyMigration] = Field(alias="companyMigration", default=None)
    invoiceShowDeliveryDate: Optional[bool] = Field(alias="invoiceShowDeliveryDate", default=None)
    customerCompanyId: Optional[int] = Field(alias="customerCompanyId", default=None)

    # Add a validator to handle empty email strings
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, dict) and "email" in obj and obj["email"] == "":
            obj["email"] = None
        return super().model_validate(obj, *args, **kwargs)


class CompanyUpdate(BaseModel):
    """Model for updating a company.

    This model includes all fields that can be updated in a company.
    For the PUT /company endpoint, id and version are required.
    """

    id: int = Field(alias="id")
    version: int = Field(alias="version")
    name: Optional[str] = Field(alias="name", default=None)
    startDate: Optional[datetime.date] = Field(alias="startDate", default=None)
    endDate: Optional[datetime.date] = Field(alias="endDate", default=None)
    organizationNumber: Optional[str] = Field(alias="organizationNumber", default=None)
    email: Optional[Union[EmailStr, str]] = Field(alias="email", default=None)
    phoneNumber: Optional[str] = Field(alias="phoneNumber", default=None)
    phoneNumberMobile: Optional[str] = Field(alias="phoneNumberMobile", default=None)
    faxNumber: Optional[str] = Field(alias="faxNumber", default=None)
    address: Optional[Address] = Field(alias="address", default=None)
    company_type: Optional[CompanyType] = Field(alias="type", default=None)  # Renamed from 'type'
    currency: Optional[Currency] = Field(alias="currency", default=None)

    # Add a validator to handle empty email strings
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, dict) and "email" in obj and obj["email"] == "":
            obj["email"] = None
        return super().model_validate(obj, *args, **kwargs)


# Response Wrappers
CompanyResponse = TripletexResponse[Company]
CompanyListResponse = TripletexResponse[List[Company]]
ClientListResponse = TripletexResponse[List[Client]]
