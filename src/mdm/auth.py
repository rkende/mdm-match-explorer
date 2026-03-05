"""Authentication and token management for IBM MDM API."""

import requests
import time
from typing import Optional, Tuple
from datetime import datetime, timedelta
import json
from pathlib import Path


class TokenManager:
    """Manages IBM Cloud IAM token lifecycle with automatic renewal."""
    
    def __init__(self, api_key: str, token_cache_file: Optional[str] = None):
        """
        Initialize the token manager.
        
        Args:
            api_key: IBM Cloud API key
            token_cache_file: Optional file path to cache tokens
        """
        self.api_key = api_key
        self.token_cache_file = token_cache_file or str(Path.home() / ".mdm_token_cache.json")
        self.current_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.iam_token_url = "https://iam.cloud.ibm.com/identity/token"
        
        # Try to load cached token
        self._load_cached_token()
    
    def get_token(self) -> str:
        """
        Get a valid bearer token, refreshing if necessary.
        
        Returns:
            Valid bearer token
            
        Raises:
            Exception: If token refresh fails
        """
        # Check if we need to refresh
        if self._needs_refresh():
            self._refresh_token()
        
        return self.current_token
    
    def _needs_refresh(self) -> bool:
        """Check if token needs to be refreshed."""
        if self.current_token is None:
            return True
        
        if self.token_expiry is None:
            return True
        
        # Refresh if token expires in less than 5 minutes
        return datetime.now() >= (self.token_expiry - timedelta(minutes=5))
    
    def _refresh_token(self) -> None:
        """Refresh the bearer token using the API key."""
        try:
            # Request new token from IBM Cloud IAM
            response = requests.post(
                self.iam_token_url,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                },
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                    "apikey": self.api_key
                },
                timeout=30
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            # Extract token and expiry
            self.current_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            # Cache the token
            self._cache_token(token_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to refresh IBM Cloud IAM token: {str(e)}")
    
    def _cache_token(self, token_data: dict) -> None:
        """Cache token data to file."""
        try:
            cache_data = {
                "access_token": token_data["access_token"],
                "expires_in": token_data.get("expires_in", 3600),
                "token_type": token_data.get("token_type", "Bearer"),
                "cached_at": datetime.now().isoformat(),
                "expires_at": self.token_expiry.isoformat() if self.token_expiry else None
            }
            
            with open(self.token_cache_file, 'w') as f:
                json.dump(cache_data, f)
                
            # Set restrictive permissions (owner read/write only)
            Path(self.token_cache_file).chmod(0o600)
            
        except Exception:
            # Silently fail if caching doesn't work
            pass
    
    def _load_cached_token(self) -> None:
        """Load cached token if available and valid."""
        try:
            if not Path(self.token_cache_file).exists():
                return
            
            with open(self.token_cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cached token is still valid
            expires_at_str = cache_data.get("expires_at")
            if expires_at_str:
                expires_at = datetime.fromisoformat(expires_at_str)
                
                # Use cached token if it's still valid for at least 5 minutes
                if datetime.now() < (expires_at - timedelta(minutes=5)):
                    self.current_token = cache_data["access_token"]
                    self.token_expiry = expires_at
                    
        except Exception:
            # Silently fail if loading cache doesn't work
            pass
    
    def clear_cache(self) -> None:
        """Clear the cached token."""
        try:
            if Path(self.token_cache_file).exists():
                Path(self.token_cache_file).unlink()
        except Exception:
            pass
    
    def get_token_info(self) -> dict:
        """
        Get information about the current token.
        
        Returns:
            Dictionary with token status information
        """
        if self.current_token is None:
            return {
                "status": "No token",
                "expires_in": None,
                "expires_at": None
            }
        
        if self.token_expiry is None:
            return {
                "status": "Token available (expiry unknown)",
                "expires_in": None,
                "expires_at": None
            }
        
        now = datetime.now()
        if now >= self.token_expiry:
            return {
                "status": "Token expired",
                "expires_in": 0,
                "expires_at": self.token_expiry.isoformat()
            }
        
        time_remaining = self.token_expiry - now
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        
        return {
            "status": "Token valid",
            "expires_in": minutes_remaining,
            "expires_at": self.token_expiry.isoformat(),
            "needs_refresh": self._needs_refresh()
        }


def validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an IBM Cloud API key by attempting to get a token.
    
    Args:
        api_key: IBM Cloud API key to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        manager = TokenManager(api_key)
        manager.get_token()
        return True, None
    except Exception as e:
        return False, str(e)

# Made with Bob
