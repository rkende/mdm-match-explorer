"""Visualization components for match results."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List, Optional


def render_match_result(match_result: Dict[str, Any]) -> None:
    """
    Render the match result with visualizations.
    
    Args:
        match_result: Match result dictionary from MDM API
    """
    # Extract key information
    match_decision = match_result.get("match_decision", "UNKNOWN")
    overall_score = match_result.get("overall_score", 0.0)
    confidence = match_result.get("confidence", "UNKNOWN")
    
    # Display overall result
    st.markdown("---")
    st.markdown("## Match Result")
    
    # Create three columns for the main result
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Match decision with color coding
        if match_decision == "MATCH":
            st.success(f"✓ {match_decision}")
        elif match_decision == "NO_MATCH":
            st.error(f"✗ {match_decision}")
        elif match_decision == "POSSIBLE_MATCH":
            st.warning(f"~ {match_decision}")
        else:
            st.info(f"? {match_decision}")
    
    with col2:
        # Overall score (similarity - match probability)
        if overall_score is not None:
            # If score is between 0-1, it's already a probability
            if 0 <= overall_score <= 1:
                score_percentage = overall_score * 100
                st.metric("Match Probability", f"{score_percentage:.1f}%")
            else:
                # If score is outside 0-1 range, show as-is
                st.metric("Match Score", f"{overall_score:.2f}")
        else:
            st.metric("Match Score", "N/A")
        
        # Show raw score if available in debug details
        raw_response = match_result.get("raw_response", {})
        if "score" in raw_response and "similarity" in raw_response:
            st.caption(f"Raw Score: {raw_response['score']:.2f}")
    
    with col3:
        # Confidence level
        st.metric("Confidence", confidence)
    
    # Score gauge chart
    render_score_gauge(overall_score)
    
    # Field comparisons
    field_comparisons = match_result.get("field_comparisons", [])
    if field_comparisons:
        st.markdown("### Field-by-Field Comparison")
        render_field_comparison_table(field_comparisons)
    
    # Debug details
    debug_details = match_result.get("debug_details")
    if debug_details:
        with st.expander("🔍 Debug Details", expanded=False):
            st.json(debug_details)
    
    # Raw response
    with st.expander("📄 Raw API Response", expanded=False):
        st.json(match_result.get("raw_response", {}))


def render_score_gauge(score: float) -> None:
    """
    Render a gauge chart for the match score.
    
    Args:
        score: Match score (0-1 or 0-100)
    """
    # Normalize score to 0-100
    score_percentage = score * 100 if score <= 1 else score
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "yellow"},
                {'range': [70, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def render_field_comparison_table(field_comparisons: List[Dict[str, Any]]) -> None:
    """
    Render a table showing field-by-field comparison.
    
    Args:
        field_comparisons: List of field comparison dictionaries
    """
    if not field_comparisons:
        st.info("No field comparison data available")
        return
    
    # Convert to DataFrame for display
    df = pd.DataFrame(field_comparisons)
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def render_field_diff(entity1: Dict[str, Any], entity2: Dict[str, Any]) -> None:
    """
    Render a side-by-side comparison of two entities with color coding.
    
    Args:
        entity1: First entity dictionary
        entity2: Second entity dictionary
    """
    st.markdown("### Entity Comparison")
    
    # Define fields to compare
    fields_to_compare = [
        ("Legal Name - Given", ["legal_name", "given_name"]),
        ("Legal Name - Middle", ["legal_name", "middle_name"]),
        ("Legal Name - Last", ["legal_name", "last_name"]),
        ("Legal Name - Prefix", ["legal_name", "prefix"]),
        ("Legal Name - Suffix", ["legal_name", "suffix"]),
        ("Birth Date", ["birth_date"]),
        ("Gender", ["gender"]),
        ("Address", ["primary_residence", "address_line1"]),
        ("City", ["primary_residence", "city"]),
        ("State/Province", ["primary_residence", "province_state"]),
        ("Zip/Postal Code", ["primary_residence", "zip_postal_code"]),
        ("Country", ["primary_residence", "country"]),
        ("Home Phone", ["home_telephone"]),
        ("Mobile Phone", ["mobile_telephone"]),
        ("Email", ["personal_email"]),
        ("SSN", ["social_security_number"]),
        ("Driver's License", ["drivers_licence"]),
        ("Passport", ["passport"])
    ]
    
    # Build comparison data
    comparison_data = []
    for field_name, field_path in fields_to_compare:
        value1 = get_nested_value(entity1, field_path)
        value2 = get_nested_value(entity2, field_path)
        
        # Determine match status
        if value1 and value2:
            if value1 == value2:
                match_status = "✓ Exact"
            else:
                match_status = "~ Different"
        elif value1 or value2:
            match_status = "✗ Missing"
        else:
            match_status = "- Empty"
        
        comparison_data.append({
            "Field": field_name,
            "Entity 1": value1 or "(empty)",
            "Entity 2": value2 or "(empty)",
            "Status": match_status
        })
    
    # Display as dataframe
    df = pd.DataFrame(comparison_data)
    
    # Apply styling
    def highlight_status(row):
        if row["Status"].startswith("✓"):
            return ['background-color: #d4edda'] * len(row)
        elif row["Status"].startswith("~"):
            return ['background-color: #fff3cd'] * len(row)
        elif row["Status"].startswith("✗"):
            return ['background-color: #f8d7da'] * len(row)
        else:
            return [''] * len(row)
    
    styled_df = df.style.apply(highlight_status, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def get_nested_value(data: Dict[str, Any], path: List[str]) -> Optional[str]:
    """
    Get a nested value from a dictionary using a path.
    
    Args:
        data: Dictionary to search
        path: List of keys representing the path
        
    Returns:
        Value at the path or None if not found
    """
    current = data
    for key in path:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return None
        else:
            return None
    
    return str(current) if current else None


def render_config_editor(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render configuration editor for query parameters.
    
    Args:
        config: Current configuration dictionary
        
    Returns:
        Updated configuration dictionary
    """
    st.markdown("### Configuration")
    
    with st.expander("Query Parameters", expanded=True):
        crn = st.text_input(
            "CRN (Cloud Resource Name)",
            value=config.get("crn", ""),
            help="Your IBM Cloud MDM instance CRN"
        )
        
        st.info("💡 **Record Numbers**: Only needed when comparing existing records in MDM. Leave empty to compare new/fictional records.")
        
        col1, col2 = st.columns(2)
        with col1:
            record_number1 = st.text_input(
                "Record Number 1 (Optional)",
                value=config.get("record_number1", ""),
                help="Leave empty for new records. Only use if comparing existing MDM records."
            )
        with col2:
            record_number2 = st.text_input(
                "Record Number 2 (Optional)",
                value=config.get("record_number2", ""),
                help="Leave empty for new records. Only use if comparing existing MDM records."
            )
        
        details = st.selectbox(
            "Details Level",
            options=["debug", "standard"],
            index=0 if config.get("details", "debug") == "debug" else 1,
            help="debug provides detailed matching information"
        )
    
    return {
        "crn": crn,
        "record_number1": record_number1,
        "record_number2": record_number2,
        "details": details
    }

# Made with Bob
