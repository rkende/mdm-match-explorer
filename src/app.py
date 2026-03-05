"""Main Streamlit application for IBM MDM Match Decision Explorer."""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from mdm.client import MDMClient
from mdm.models import (
    PersonRecord, PersonAttributes, LegalName, BirthDate, Gender,
    PrimaryResidence, Telephone, Email, Identification, CompareRequest
)
from ui.entity_input import render_entity_form, validate_entity
from ui.visualizations import (
    render_match_result, render_field_diff, render_config_editor
)
from ui.sample_data import get_sample_data_manager
from utils.config import get_config, validate_config


def load_entity_to_session_state(entity: dict, key_prefix: str) -> None:
    """
    Load entity data into Streamlit session state widget keys.
    
    Args:
        entity: Entity dictionary
        key_prefix: Prefix for widget keys (entity1 or entity2)
    """
    # Record metadata
    st.session_state[f"{key_prefix}_record_source"] = entity.get("record_source", "MDM")
    st.session_state[f"{key_prefix}_record_id"] = entity.get("record_id", "")
    
    # Legal name
    legal_name = entity.get("legal_name", {})
    st.session_state[f"{key_prefix}_prefix"] = legal_name.get("prefix", "")
    st.session_state[f"{key_prefix}_given_name"] = legal_name.get("given_name", "")
    st.session_state[f"{key_prefix}_middle_name"] = legal_name.get("middle_name", "")
    st.session_state[f"{key_prefix}_last_name"] = legal_name.get("last_name", "")
    st.session_state[f"{key_prefix}_suffix"] = legal_name.get("suffix", "")
    st.session_state[f"{key_prefix}_generation"] = legal_name.get("generation", "")
    
    # Demographics
    st.session_state[f"{key_prefix}_birth_date"] = entity.get("birth_date", "")
    st.session_state[f"{key_prefix}_gender"] = entity.get("gender", "")
    
    # Primary residence
    residence = entity.get("primary_residence", {})
    st.session_state[f"{key_prefix}_address_line1"] = residence.get("address_line1", "")
    st.session_state[f"{key_prefix}_city"] = residence.get("city", "")
    st.session_state[f"{key_prefix}_province_state"] = residence.get("province_state", "")
    st.session_state[f"{key_prefix}_zip_postal_code"] = residence.get("zip_postal_code", "")
    st.session_state[f"{key_prefix}_country"] = residence.get("country", "")
    st.session_state[f"{key_prefix}_county"] = residence.get("county", "")
    st.session_state[f"{key_prefix}_residence_number"] = residence.get("residence_number", "")
    st.session_state[f"{key_prefix}_residence_type"] = residence.get("residence", "")
    
    # Contact information
    st.session_state[f"{key_prefix}_home_telephone"] = entity.get("home_telephone", "")
    st.session_state[f"{key_prefix}_mobile_telephone"] = entity.get("mobile_telephone", "")
    st.session_state[f"{key_prefix}_personal_email"] = entity.get("personal_email", "")
    
    # Identifications
    st.session_state[f"{key_prefix}_ssn"] = entity.get("social_security_number", "")
    st.session_state[f"{key_prefix}_drivers_licence"] = entity.get("drivers_licence", "")
    st.session_state[f"{key_prefix}_passport"] = entity.get("passport", "")


def convert_entity_to_mdm_format(entity: dict) -> PersonAttributes:
    """
    Convert simplified entity format to MDM API format.
    
    Args:
        entity: Simplified entity dictionary from form
        
    Returns:
        PersonAttributes object for API request
    """
    # Build legal name
    legal_name_data = entity.get("legal_name", {})
    legal_name = None
    if any(legal_name_data.values()):
        legal_name = [LegalName(**legal_name_data)]
    
    # Build birth date
    birth_date = None
    if entity.get("birth_date"):
        birth_date = [BirthDate(value=entity["birth_date"] + "T00:00:00")]
    
    # Build gender
    gender = None
    if entity.get("gender"):
        gender = [Gender(value=entity["gender"])]
    
    # Build primary residence
    residence_data = entity.get("primary_residence", {})
    primary_residence = None
    if any(residence_data.values()):
        primary_residence = [PrimaryResidence(**residence_data)]
    
    # Build telephones
    home_telephone = None
    if entity.get("home_telephone"):
        home_telephone = [Telephone(
            phone_number=entity["home_telephone"],
            contact_method="Telephone Number"
        )]
    
    mobile_telephone = None
    if entity.get("mobile_telephone"):
        mobile_telephone = [Telephone(
            phone_number=entity["mobile_telephone"],
            contact_method="Telephone Number"
        )]
    
    # Build email
    personal_email = None
    if entity.get("personal_email"):
        personal_email = [Email(
            email_id=entity["personal_email"],
            usageValue="personal_email"
        )]
    
    # Build identifications
    ssn = None
    if entity.get("social_security_number"):
        ssn = [Identification(
            identification_number=entity["social_security_number"],
            usageValue="social_security_number"
        )]
    
    drivers_licence = None
    if entity.get("drivers_licence"):
        drivers_licence = [Identification(
            identification_number=entity["drivers_licence"],
            usageValue="drivers_licence"
        )]
    
    passport = None
    if entity.get("passport"):
        passport = [Identification(
            identification_number=entity["passport"],
            usageValue="passport"
        )]
    
    # Create PersonAttributes
    return PersonAttributes(
        record_source=entity.get("record_source", "MDM"),
        record_id=entity.get("record_id", ""),
        record_last_updated=entity.get("record_last_updated", ""),
        birth_date=birth_date,
        gender=gender,
        primary_residence=primary_residence,
        home_telephone=home_telephone,
        mobile_telephone=mobile_telephone,
        personal_email=personal_email,
        social_security_number=ssn,
        drivers_licence=drivers_licence,
        passport=passport,
        legal_name=legal_name
    )


def main():
    """Main application entry point."""
    
    # Page configuration
    config = get_config()
    st.set_page_config(
        page_title=config.app_title,
        page_icon=config.app_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title
    st.title(f"{config.app_icon} {config.app_title}")
    st.markdown("Compare two entity records and explore MDM matching decisions in real-time")
    
    # Validate configuration
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(f"⚠️ Configuration Error: {error_msg}")
        st.info("Please create a `.env` file based on `.env.example` and configure your MDM credentials.")
        st.stop()
    
    # Initialize session state
    if "entity1_data" not in st.session_state:
        st.session_state.entity1_data = get_sample_data_manager().get_empty_entity()
    if "entity2_data" not in st.session_state:
        st.session_state.entity2_data = get_sample_data_manager().get_empty_entity()
    if "match_result" not in st.session_state:
        st.session_state.match_result = None
    if "config_params" not in st.session_state:
        st.session_state.config_params = {
            "crn": config.mdm_crn,
            "record_number1": "",  # Empty by default for new/fictional records
            "record_number2": "",  # Empty by default for new/fictional records
            "details": "debug"
        }
    
    # Sidebar - Configuration and Sample Data
    with st.sidebar:
        st.header("Configuration")
        
        # Show token status if using API key
        if config.mdm_api_key:
            client = MDMClient()
            if client.token_manager:
                token_info = client.token_manager.get_token_info()
                if token_info["status"] == "Token valid":
                    st.success(f"🔑 Token valid ({token_info['expires_in']} min remaining)")
                elif token_info["status"] == "Token expired":
                    st.warning("🔑 Token expired (will auto-refresh)")
                else:
                    st.info(f"🔑 {token_info['status']}")
        
        # Configuration editor
        st.session_state.config_params = render_config_editor(st.session_state.config_params)
        
        st.markdown("---")
        st.header("Sample Data")
        
        # Sample data selector
        sample_manager = get_sample_data_manager()
        scenario_names = ["(None)"] + sample_manager.get_scenario_names()
        
        selected_scenario = st.selectbox(
            "Load Sample Scenario",
            options=scenario_names,
            key="sample_scenario_selector"
        )
        
        if selected_scenario != "(None)":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load to Entity 1", use_container_width=True):
                    entity = sample_manager.get_entity_from_scenario(selected_scenario, 1)
                    if entity:
                        # Update session state data
                        st.session_state.entity1_data = entity
                        # Update all widget session state keys
                        load_entity_to_session_state(entity, "entity1")
                        st.rerun()
            with col2:
                if st.button("Load to Entity 2", use_container_width=True):
                    entity = sample_manager.get_entity_from_scenario(selected_scenario, 2)
                    if entity:
                        # Update session state data
                        st.session_state.entity2_data = entity
                        # Update all widget session state keys
                        load_entity_to_session_state(entity, "entity2")
                        st.rerun()
            
            # Show scenario description
            scenario = sample_manager.get_scenario(selected_scenario)
            if scenario:
                st.info(f"**{scenario['name']}**\n\n{scenario['description']}")
        
        st.markdown("---")
        
        # Clear button
        if st.button("🗑️ Clear All Data", use_container_width=True):
            empty_entity = sample_manager.get_empty_entity()
            st.session_state.entity1_data = empty_entity
            st.session_state.entity2_data = empty_entity
            st.session_state.match_result = None
            # Clear all widget session state keys
            load_entity_to_session_state(empty_entity, "entity1")
            load_entity_to_session_state(empty_entity, "entity2")
            st.rerun()
    
    # Main content - Entity input forms
    col1, col2 = st.columns(2)
    
    with col1:
        entity1 = render_entity_form(
            st.session_state.get("entity1_data", get_sample_data_manager().get_empty_entity()),
            entity_number=1,
            key_prefix="entity1"
        )
    
    with col2:
        entity2 = render_entity_form(
            st.session_state.get("entity2_data", get_sample_data_manager().get_empty_entity()),
            entity_number=2,
            key_prefix="entity2"
        )
    
    # Update session state with current form values
    st.session_state.entity1_data = entity1
    st.session_state.entity2_data = entity2
    
    # Compare button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        compare_button = st.button(
            "🔍 Compare Entities",
            use_container_width=True,
            type="primary"
        )
    
    # Process comparison
    if compare_button:
        # Validate entities
        is_valid1, error1 = validate_entity(entity1)
        is_valid2, error2 = validate_entity(entity2)
        
        if not is_valid1:
            st.error(f"Entity 1 validation error: {error1}")
            st.stop()
        
        if not is_valid2:
            st.error(f"Entity 2 validation error: {error2}")
            st.stop()
        
        # Show progress
        with st.spinner("Comparing entities via MDM API..."):
            try:
                # Initialize MDM client
                client = MDMClient()
                
                # Convert entities to MDM format
                person1_attrs = convert_entity_to_mdm_format(entity1)
                person2_attrs = convert_entity_to_mdm_format(entity2)
                
                # Create records
                record1 = PersonRecord(record_type="person", attributes=person1_attrs)
                record2 = PersonRecord(record_type="person", attributes=person2_attrs)
                
                # Create compare request
                compare_request = CompareRequest(records=[record1, record2])
                
                # Debug: Show request body if debug mode is enabled
                if config.debug_mode:
                    st.write("**Debug: Request Body**")
                    st.json(compare_request.model_dump(exclude_none=True))
                
                # Make API call
                response = client.compare_entities(
                    request=compare_request,
                    crn=st.session_state.config_params["crn"],
                    entity_type=config.mdm_entity_type,
                    record_type=config.mdm_record_type,
                    record_number1=st.session_state.config_params["record_number1"],
                    record_number2=st.session_state.config_params["record_number2"],
                    details=st.session_state.config_params["details"]
                )
                
                # Process result
                match_result = client.process_match_result(response)
                st.session_state.match_result = match_result.model_dump()
                
                st.success("✓ Comparison complete!")
                
            except Exception as e:
                st.error(f"❌ Error during comparison: {str(e)}")
                if config.debug_mode:
                    st.exception(e)
                st.stop()
    
    # Display results
    if st.session_state.match_result:
        render_match_result(st.session_state.match_result)
        
        st.markdown("---")
        render_field_diff(entity1, entity2)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.8em;'>
        IBM MDM Match Decision Explorer v1.0.0 | 
        Built with Streamlit | 
        Powered by IBM MDM (Match 360)
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

# Made with Bob
