"""Data models for MDM API requests and responses."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class LegalName(BaseModel):
    """Legal name structure."""
    record_start: Optional[str] = None
    record_last_updated: Optional[str] = None
    generation: Optional[str] = None
    usage: Optional[str] = "Legal"
    prefix: Optional[str] = None
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    suffix: Optional[str] = None


class BirthDate(BaseModel):
    """Birth date structure."""
    value: Optional[str] = None


class Gender(BaseModel):
    """Gender structure."""
    value: Optional[str] = None


class PrimaryResidence(BaseModel):
    """Primary residence structure."""
    record_start: Optional[str] = None
    record_last_updated: Optional[str] = None
    residence: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    zip_postal_code: Optional[str] = None
    residence_number: Optional[str] = None
    province_state: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None


class Telephone(BaseModel):
    """Telephone structure."""
    record_start: Optional[str] = None
    record_last_updated: Optional[str] = None
    phone_number: Optional[str] = None
    contact_method: Optional[str] = "Telephone Number"


class Email(BaseModel):
    """Email structure."""
    record_last_updated: Optional[str] = None
    usageValue: Optional[str] = "personal_email"
    email_id: Optional[str] = None
    record_start: Optional[str] = None
    usageType: Optional[str] = "6"


class Identification(BaseModel):
    """Identification structure (SSN, Driver's License, Passport)."""
    record_last_updated: Optional[str] = None
    usageValue: Optional[str] = None
    identification_number: Optional[str] = None
    record_start: Optional[str] = None
    usageType: Optional[str] = "6"


class PersonAttributes(BaseModel):
    """Person entity attributes."""
    record_source: Optional[str] = "MDM"
    record_id: Optional[str] = None
    record_last_updated: Optional[int] = None  # Unix timestamp in milliseconds
    birth_date: Optional[List[BirthDate]] = None
    gender: Optional[List[Gender]] = None
    primary_residence: Optional[List[PrimaryResidence]] = None
    home_telephone: Optional[List[Telephone]] = None
    mobile_telephone: Optional[List[Telephone]] = None
    personal_email: Optional[List[Email]] = None
    social_security_number: Optional[List[Identification]] = None
    drivers_licence: Optional[List[Identification]] = None
    passport: Optional[List[Identification]] = None
    legal_name: Optional[List[LegalName]] = None


class PersonRecord(BaseModel):
    """Person record structure."""
    record_type: str = "person"
    attributes: PersonAttributes


class CompareRequest(BaseModel):
    """MDM compare API request."""
    records: List[PersonRecord]


class CompareResponse(BaseModel):
    """MDM compare API response."""
    # The actual response structure will be determined from API responses
    # This is a placeholder that will be updated based on actual data
    raw_response: Dict[str, Any] = Field(default_factory=dict)
    match_decision: Optional[str] = None
    overall_score: Optional[float] = None
    confidence: Optional[str] = None
    field_comparisons: Optional[List[Dict[str, Any]]] = None
    debug_details: Optional[Dict[str, Any]] = None


class MatchResult(BaseModel):
    """Processed match result for UI display."""
    match_decision: str
    overall_score: float
    confidence: str
    field_comparisons: List[Dict[str, Any]]
    debug_details: Optional[Dict[str, Any]] = None
    raw_response: Dict[str, Any]

# Made with Bob
