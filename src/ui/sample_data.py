"""Sample data management for the application."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class SampleDataManager:
    """Manages sample entity data for quick testing."""
    
    def __init__(self, sample_file_path: Optional[str] = None):
        """
        Initialize the sample data manager.
        
        Args:
            sample_file_path: Path to the sample entities JSON file
        """
        if sample_file_path is None:
            # Default to config/sample_entities.json
            current_dir = Path(__file__).parent.parent.parent
            sample_file_path = current_dir / "config" / "sample_entities.json"
        
        self.sample_file_path = Path(sample_file_path)
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> List[Dict[str, Any]]:
        """Load sample scenarios from JSON file."""
        try:
            with open(self.sample_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("scenarios", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def get_scenario_names(self) -> List[str]:
        """Get list of available scenario names."""
        return [scenario["name"] for scenario in self.scenarios]
    
    def get_scenario(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a scenario by name.
        
        Args:
            name: Name of the scenario
            
        Returns:
            Scenario dictionary or None if not found
        """
        for scenario in self.scenarios:
            if scenario["name"] == name:
                return scenario
        return None
    
    def get_entity_from_scenario(self, scenario_name: str, entity_number: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific entity from a scenario.
        
        Args:
            scenario_name: Name of the scenario
            entity_number: 1 for entity1, 2 for entity2
            
        Returns:
            Entity dictionary or None if not found
        """
        scenario = self.get_scenario(scenario_name)
        if scenario is None:
            return None
        
        entity_key = f"entity{entity_number}"
        return scenario.get(entity_key)
    
    def get_empty_entity(self) -> Dict[str, Any]:
        """Get an empty entity template."""
        return {
            "record_source": "MDM",
            "record_id": "",
            "birth_date": "",
            "gender": "",
            "legal_name": {
                "given_name": "",
                "middle_name": "",
                "last_name": "",
                "prefix": "",
                "suffix": "",
                "generation": ""
            },
            "primary_residence": {
                "address_line1": "",
                "city": "",
                "province_state": "",
                "zip_postal_code": "",
                "country": "",
                "county": "",
                "residence_number": "",
                "residence": ""
            },
            "home_telephone": "",
            "mobile_telephone": "",
            "personal_email": "",
            "social_security_number": "",
            "drivers_licence": "",
            "passport": ""
        }


# Global instance
_sample_data_manager = None


def get_sample_data_manager() -> SampleDataManager:
    """Get the global sample data manager instance."""
    global _sample_data_manager
    if _sample_data_manager is None:
        _sample_data_manager = SampleDataManager()
    return _sample_data_manager

# Made with Bob
