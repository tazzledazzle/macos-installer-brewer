from abc import ABC, abstractmethod
from typing import Dict, Optional
import logging
import os

class BaseBuilder(ABC):
    def __init__(self, config: Dict, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger(__name__)

    def ensure_output_directory(self) -> None:
        """Ensure the output directory exists."""
        os.makedirs(self.config['outputDir'], exist_ok=True)

    @abstractmethod
    def build(self) -> str:
        """Build the installer."""
        pass