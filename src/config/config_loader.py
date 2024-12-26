import json
from typing import Dict
import logging

class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> Dict:
        """Load and validate configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                ConfigLoader._validate_config(config)
                return config
        except Exception as e:
            raise ValueError(f"Failed to load config: {str(e)}")

    @staticmethod
    def _validate_config(config: Dict) -> None:
        """Validate required configuration fields."""
        required_fields = ['appName', 'version', 'identifier', 'outputDir']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required config fields: {', '.join(missing_fields)}")