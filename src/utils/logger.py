import logging
from typing import Optional

class Logger:
    _instance: Optional[logging.Logger] = None

    @staticmethod
    def setup(name: str = 'InstallerBuilder') -> logging.Logger:
        """Setup and return a singleton logger instance."""
        if Logger._instance is None:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            Logger._instance = logging.getLogger(name)
        return Logger._instance