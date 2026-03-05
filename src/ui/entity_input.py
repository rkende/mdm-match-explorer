"""Entity input forms for the Streamlit UI."""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime


def render_entity_form(
    entity_data: Dict[str, Any],
    entity_number: int,
    key_prefix: str
) -> Dict[str, Any]:
    """
    Render an entity input form.
    
    Args:
        entity_data: Initial entity data
        entity_number: 1 or 2 (for labeling)
        key_prefix: Prefix for Streamlit widget keys
        
    Returns:
        Dictionary with entity data from form inputs
    """
    st.subheader(f"Entity {entity_number}")
    
    # Initialize session state keys if they don't exist
    legal_name = entity_data.get("legal_name", {})
    residence = entity_data.get("primary_residence", {})
    
    # Helper function to get value from session state or entity_data
    def get_value(key, default=""):
        session_key = f"{key_prefix}_{key}"
        if session_key not in st.session_state:
            st.session_state[session_key] = default
        return st.session_state[session_key]
    
    # Record metadata
    with st.expander("Record Metadata", expanded=False):
        record_source = st.text_input(
            "Record Source",
            value=entity_data.get("record_source", "MDM"),
            key=f"{key_prefix}_record_source"
        )
        record_id = st.text_input(
            "Record ID",
            value=entity_data.get("record_id", ""),
            key=f"{key_prefix}_record_id"
        )
    
    # Legal Name
    st.markdown("**Legal Name**")
    
    col1, col2 = st.columns(2)
    with col1:
        prefix = st.text_input(
            "Prefix",
            value=legal_name.get("prefix", ""),
            key=f"{key_prefix}_prefix",
            placeholder="Mr, Ms, Dr, Rev"
        )
        given_name = st.text_input(
            "Given Name *",
            value=legal_name.get("given_name", ""),
            key=f"{key_prefix}_given_name"
        )
        last_name = st.text_input(
            "Last Name *",
            value=legal_name.get("last_name", ""),
            key=f"{key_prefix}_last_name"
        )
    
    with col2:
        middle_name = st.text_input(
            "Middle Name",
            value=legal_name.get("middle_name", ""),
            key=f"{key_prefix}_middle_name"
        )
        suffix = st.text_input(
            "Suffix",
            value=legal_name.get("suffix", ""),
            key=f"{key_prefix}_suffix",
            placeholder="Jr, Sr, II, III"
        )
        generation = st.text_input(
            "Generation",
            value=legal_name.get("generation", ""),
            key=f"{key_prefix}_generation",
            placeholder="PhD, MD"
        )
    
    # Demographics
    st.markdown("**Demographics**")
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.text_input(
            "Birth Date",
            value=entity_data.get("birth_date", ""),
            key=f"{key_prefix}_birth_date",
            placeholder="YYYY-MM-DD"
        )
    with col2:
        gender = st.selectbox(
            "Gender",
            options=["", "Male", "Female", "Other"],
            index=0 if not entity_data.get("gender") else 
                  ["", "Male", "Female", "Other"].index(entity_data.get("gender", "")),
            key=f"{key_prefix}_gender"
        )
    
    # Primary Residence
    st.markdown("**Primary Residence**")
    residence = entity_data.get("primary_residence", {})
    
    address_line1 = st.text_input(
        "Address Line 1",
        value=residence.get("address_line1", ""),
        key=f"{key_prefix}_address_line1"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input(
            "City",
            value=residence.get("city", ""),
            key=f"{key_prefix}_city"
        )
    with col2:
        province_state = st.text_input(
            "Province/State",
            value=residence.get("province_state", ""),
            key=f"{key_prefix}_province_state"
        )
    with col3:
        zip_postal_code = st.text_input(
            "Zip/Postal Code",
            value=residence.get("zip_postal_code", ""),
            key=f"{key_prefix}_zip_postal_code"
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.text_input(
            "Country",
            value=residence.get("country", ""),
            key=f"{key_prefix}_country"
        )
    with col2:
        county = st.text_input(
            "County",
            value=residence.get("county", ""),
            key=f"{key_prefix}_county"
        )
    with col3:
        residence_number = st.text_input(
            "Residence Number",
            value=residence.get("residence_number", ""),
            key=f"{key_prefix}_residence_number"
        )
    
    residence_type = st.text_input(
        "Residence Type",
        value=residence.get("residence", ""),
        key=f"{key_prefix}_residence_type",
        placeholder="house, apartment, condo"
    )
    
    # Contact Information
    st.markdown("**Contact Information**")
    col1, col2 = st.columns(2)
    with col1:
        home_telephone = st.text_input(
            "Home Telephone",
            value=entity_data.get("home_telephone", ""),
            key=f"{key_prefix}_home_telephone"
        )
        personal_email = st.text_input(
            "Personal Email",
            value=entity_data.get("personal_email", ""),
            key=f"{key_prefix}_personal_email"
        )
    with col2:
        mobile_telephone = st.text_input(
            "Mobile Telephone",
            value=entity_data.get("mobile_telephone", ""),
            key=f"{key_prefix}_mobile_telephone"
        )
    
    # Identifications
    st.markdown("**Identifications**")
    col1, col2, col3 = st.columns(3)
    with col1:
        ssn = st.text_input(
            "Social Security Number",
            value=entity_data.get("social_security_number", ""),
            key=f"{key_prefix}_ssn",
            type="password"
        )
    with col2:
        drivers_licence = st.text_input(
            "Driver's License",
            value=entity_data.get("drivers_licence", ""),
            key=f"{key_prefix}_drivers_licence"
        )
    with col3:
        passport = st.text_input(
            "Passport",
            value=entity_data.get("passport", ""),
            key=f"{key_prefix}_passport"
        )
    
    # Build the entity dictionary
    # Convert current time to Unix timestamp in milliseconds (integer)
    current_timestamp_ms = int(datetime.now().timestamp() * 1000)
    current_timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    entity = {
        "record_source": record_source,
        "record_id": record_id,
        "record_last_updated": current_timestamp_ms,
        "birth_date": birth_date,
        "gender": gender,
        "legal_name": {
            "given_name": given_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "prefix": prefix,
            "suffix": suffix,
            "generation": generation,
            "usage": "Legal",
            "record_start": current_timestamp_str,
            "record_last_updated": current_timestamp_str
        },
        "primary_residence": {
            "address_line1": address_line1,
            "city": city,
            "province_state": province_state,
            "zip_postal_code": zip_postal_code,
            "country": country,
            "county": county,
            "residence_number": residence_number,
            "residence": residence_type,
            "record_start": current_timestamp_str,
            "record_last_updated": current_timestamp_str
        },
        "home_telephone": home_telephone,
        "mobile_telephone": mobile_telephone,
        "personal_email": personal_email,
        "social_security_number": ssn,
        "drivers_licence": drivers_licence,
        "passport": passport
    }
    
    return entity


def validate_entity(entity: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate entity data.
    
    Args:
        entity: Entity dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    legal_name = entity.get("legal_name", {})
    
    if not legal_name.get("given_name"):
        return False, "Given name is required"
    
    if not legal_name.get("last_name"):
        return False, "Last name is required"
    
    return True, None

# Made with Bob
