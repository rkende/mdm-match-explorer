"""Configuration management for the MDM Match Explorer application."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AppConfig(BaseModel):
    """Application configuration."""
    
    # MDM API Configuration
    mdm_api_base_url: str = Field(
        default_factory=lambda: os.getenv(
            "MDM_API_BASE_URL",
            "https://mdm-api.match-prod-tor-f68b5e114c38aea75a77442f7486d91d-0001.ca-tor.containers.appdomain.cloud"
        )
    )
    # Support both API key (preferred) and direct bearer token (legacy)
    mdm_api_key: str = Field(
        default_factory=lambda: os.getenv("MDM_API_KEY", "")
    )
    mdm_api_token: str = Field(
        default_factory=lambda: os.getenv("MDM_API_TOKEN", "")
    )
    
    # MDM Instance Configuration
    mdm_crn: str = Field(
        default_factory=lambda: os.getenv(
            "MDM_CRN",
            "crn:v1:bluemix:public:mdm-oc:us-south:a/122c69f0e8296804c9eebf4dbd4530e4:f4d408e3-25ec-4d48-87fe-ac82018c3b32::"
        )
    )
    mdm_entity_type: str = Field(
        default_factory=lambda: os.getenv("MDM_ENTITY_TYPE", "person_entity")
    )
    mdm_record_type: str = Field(
        default_factory=lambda: os.getenv("MDM_RECORD_TYPE", "person")
    )
    
    # App Configuration
    app_title: str = Field(
        default_factory=lambda: os.getenv("APP_TITLE", "IBM MDM Match Decision Explorer")
    )
    app_icon: str = Field(
        default_factory=lambda: os.getenv("APP_ICON", "🔍")
    )
    debug_mode: bool = Field(
        default_factory=lambda: os.getenv("DEBUG_MODE", "false").lower() == "true"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global configuration instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the application configuration."""
    return config


def validate_config() -> tuple[bool, Optional[str]]:
    """
    Validate the configuration.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if either API key or token is provided
    if not config.mdm_api_key and not config.mdm_api_token:
        return False, "Neither MDM_API_KEY nor MDM_API_TOKEN is set. Please configure your IBM Cloud API key (recommended) or Bearer token in .env file."
    
    if not config.mdm_api_base_url:
        return False, "MDM_API_BASE_URL is not set."
    
    if not config.mdm_crn:
        return False, "MDM_CRN is not set."
    
    return True, None

# Made with Bob
