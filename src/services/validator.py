from typing import List, Dict
import logging

class InstallerValidator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def validate(self, installer_path: str, macos_versions: List[str]) -> bool:
        """Validate installer compatibility across macOS versions."""
        self.logger.info(f"Validating installer: {installer_path}")

        for version in macos_versions:
            self.logger.info(f"Testing on macOS {version}")
            if not self._validate_on_version(installer_path, version):
                return False
        return True

    def _validate_on_version(self, installer_path: str, version: str) -> bool:
        """Validate installer on specific macOS version."""
        # Implement validation logic using VMs or CI tools
        return True