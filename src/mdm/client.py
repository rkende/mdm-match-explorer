"""MDM API client for making compare requests."""

import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import json

from .models import CompareRequest, CompareResponse, MatchResult
from .auth import TokenManager
from utils.config import get_config


def convert_mdm_record_to_entity(record_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MDM API record response to entity format used by the application.
    
    Args:
        record_data: Record data from MDM API /records/{id} endpoint
        
    Returns:
        Entity dictionary in application format
    """
    record = record_data.get("record", {})
    attributes = record.get("attributes", {})
    
    # Extract legal name
    legal_name_data = attributes.get("legal_name", {})
    legal_name = {
        "given_name": legal_name_data.get("given_name", ""),
        "middle_name": legal_name_data.get("middle_name", ""),
        "last_name": legal_name_data.get("last_name", ""),
        "prefix": legal_name_data.get("prefix", ""),
        "suffix": legal_name_data.get("suffix", ""),
        "generation": legal_name_data.get("generation", "")
    }
    
    # Extract primary residence
    residence_data = attributes.get("primary_residence", {})
    primary_residence = {
        "address_line1": residence_data.get("address_line1", ""),
        "city": residence_data.get("city", ""),
        "province_state": residence_data.get("province_state", ""),
        "zip_postal_code": residence_data.get("zip_postal_code", ""),
        "country": residence_data.get("country", ""),
        "county": residence_data.get("county", ""),
        "residence_number": residence_data.get("residence_number", ""),
        "residence": residence_data.get("residence_type", "")
    }
    
    # Extract contact information
    home_phone = attributes.get("home_telephone", {})
    mobile_phone = attributes.get("mobile_telephone", {})
    
    # Extract identifications
    ssn_data = attributes.get("social_insurance_number", {})
    
    # Build entity dictionary
    # Get record_last_updated from record metadata or use current timestamp
    from datetime import datetime
    record_last_updated = record.get("record_last_updated")
    if not record_last_updated:
        # If not provided, use current timestamp in milliseconds
        record_last_updated = int(datetime.now().timestamp() * 1000)
    
    entity = {
        "record_source": attributes.get("record_source", "MDM"),
        "record_id": attributes.get("record_id", ""),
        "record_number": attributes.get("record_number", ""),
        "record_last_updated": record_last_updated,
        "birth_date": attributes.get("birth_date", {}).get("value", ""),
        "gender": attributes.get("gender", {}).get("value", ""),
        "legal_name": legal_name,
        "primary_residence": primary_residence,
        "home_telephone": home_phone.get("phone_number", ""),
        "mobile_telephone": mobile_phone.get("phone_number", ""),
        "personal_email": attributes.get("personal_email", {}).get("email_id", ""),
        "social_security_number": ssn_data.get("identification_number", ""),
        "drivers_licence": attributes.get("drivers_license_number", {}).get("identification_number", ""),
        "passport": attributes.get("passport_number", {}).get("identification_number", "")
    }
    
    return entity


class MDMClient:
    """Client for interacting with IBM MDM Match API."""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the MDM client.
        
        Args:
            base_url: MDM API base URL (defaults to config)
            token: Bearer token for authentication (defaults to config, legacy)
            api_key: IBM Cloud API key for automatic token management (preferred)
        """
        config = get_config()
        self.base_url = base_url or config.mdm_api_base_url
        self.timeout = 30
        
        # Initialize token manager if API key is provided
        self.token_manager: Optional[TokenManager] = None
        if api_key or config.mdm_api_key:
            self.token_manager = TokenManager(api_key or config.mdm_api_key)
            self.token = None  # Will be fetched from token manager
        else:
            # Fall back to direct token (legacy)
            self.token = token or config.mdm_api_token
            self.token_manager = None
        
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        # Get token from manager if available, otherwise use direct token
        if self.token_manager:
            token = self.token_manager.get_token()
        else:
            token = self.token
            
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def compare_entities(
        self,
        request: CompareRequest,
        crn: str,
        entity_type: str,
        record_type: str,
        record_number1: Optional[str] = None,
        record_number2: Optional[str] = None,
        details: str = "debug"
    ) -> CompareResponse:
        """
        Compare two entities using the MDM API.
        
        Args:
            request: CompareRequest containing the two entities
            crn: Cloud Resource Name
            entity_type: Type of entity (e.g., "person_entity")
            record_type: Record type (e.g., "person")
            record_number1: First record identifier (optional, for existing records)
            record_number2: Second record identifier (optional, for existing records)
            details: Detail level ("debug" for detailed output)
            
        Returns:
            CompareResponse with match results
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        # Build query parameters (exclude record numbers if not provided)
        params = {
            "crn": crn,
            "entity_type": entity_type,
            "record_type": record_type,
            "details": details
        }
        
        # Only add record numbers if they are provided and not empty
        if record_number1:
            params["record_number1"] = record_number1
        if record_number2:
            params["record_number2"] = record_number2
        
        # Build URL
        url = f"{self.base_url}/mdm/v1/compare?{urlencode(params)}"
        
        # Prepare request body
        body = request.model_dump(exclude_none=True)
        
        # Make request
        response = requests.post(
            url,
            headers=self._get_headers(),
            json=body,
            timeout=self.timeout
        )
        
        # Check for errors and provide detailed message
        if not response.ok:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = f"\nAPI Error Details: {error_data}"
            except:
                error_detail = f"\nResponse Text: {response.text}"
            
            raise requests.exceptions.HTTPError(
                f"{response.status_code} {response.reason} for url: {url}{error_detail}",
                response=response
            )
        
        # Parse response
        response_data = response.json()
        
        # Create CompareResponse with raw data
        return CompareResponse(
            raw_response=response_data,
            match_decision=self._extract_match_decision(response_data),
            overall_score=self._extract_overall_score(response_data),
            confidence=self._extract_confidence(response_data),
            field_comparisons=self._extract_field_comparisons(response_data),
            debug_details=response_data if details == "debug" else None
        )
    
    def _extract_match_decision(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract match decision from response."""
        # This will be implemented based on actual API response structure
        # Placeholder logic
        if "match_decision" in response:
            return response["match_decision"]
        elif "decision" in response:
            return response["decision"]
        elif "result" in response:
            return response["result"]
        return "UNKNOWN"
    
    def _extract_overall_score(self, response: Dict[str, Any]) -> Optional[float]:
        """
        Extract overall match score from response.
        
        Prioritizes 'similarity' (match probability 0-1) over 'score' (absolute value).
        """
        # Prioritize similarity as it represents match probability (0-1)
        if "similarity" in response:
            return float(response["similarity"])
        elif "match_score" in response:
            return float(response["match_score"])
        elif "overall_score" in response:
            return float(response["overall_score"])
        elif "score" in response:
            # Score is absolute value (can be negative), use as fallback only
            return float(response["score"])
        return None
    
    def _extract_confidence(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract confidence level from response."""
        # Placeholder logic
        if "confidence" in response:
            return response["confidence"]
        elif "confidence_level" in response:
            return response["confidence_level"]
        return "UNKNOWN"
    
    def _extract_field_comparisons(self, response: Dict[str, Any]) -> Optional[list]:
        """Extract field-level comparison details from response."""
        # Placeholder logic - will be updated based on actual response
        if "field_comparisons" in response:
            return response["field_comparisons"]
        elif "fields" in response:
            return response["fields"]
        elif "comparisons" in response:
            return response["comparisons"]
        return []
    
    def process_match_result(self, response: CompareResponse) -> MatchResult:
        """
        Process the API response into a user-friendly match result.
        
        Args:
            response: CompareResponse from the API
            
        Returns:
            MatchResult with processed data for UI display
        """
        return MatchResult(
            match_decision=response.match_decision or "UNKNOWN",
            overall_score=response.overall_score or 0.0,
            confidence=response.confidence or "UNKNOWN",
            field_comparisons=response.field_comparisons or [],
            debug_details=response.debug_details,
            raw_response=response.raw_response
        )
    
    def get_record_by_id(self, record_id: str, crn: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record by its ID from the MDM API.
        
        Args:
            record_id: The record ID to retrieve
            crn: Cloud Resource Name
            
        Returns:
            Dictionary with record data or None if not found
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        # Build query parameters
        params = {"crn": crn}
        
        # Build URL
        url = f"{self.base_url}/mdm/v1/records/{record_id}?{urlencode(params)}"
        
        # Make request
        response = requests.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        # Check for errors
        if not response.ok:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = f"\nAPI Error Details: {error_data}"
            except:
                error_detail = f"\nResponse Text: {response.text}"
            
            raise requests.exceptions.HTTPError(
                f"{response.status_code} {response.reason} for url: {url}{error_detail}",
                response=response
            )
        
        # Parse and return response
        return response.json()
    
    def test_connection(self) -> tuple[bool, Optional[str]]:
        """
        Test the connection to the MDM API.
        
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Simple health check - try to make a request with minimal data
            headers = self._get_headers()
            response = requests.get(
                f"{self.base_url}/mdm/v1/health",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, None
            else:
                return False, f"API returned status code {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

# Made with Bob
