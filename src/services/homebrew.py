import os
from typing import Dict
import logging

class HomebrewFormulaGenerator:
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def generate(self, repo_url: str) -> str:
        """Generate Homebrew formula."""
        self.logger.info("Generating Homebrew formula")

        formula_content = self._generate_formula_content(repo_url)
        formula_path = self._write_formula(formula_content)

        self.logger.info(f"Created Homebrew formula at {formula_path}")
        return formula_path

    def _generate_formula_content(self, repo_url: str) -> str:
        """Generate the formula content."""
        return f"""
class {self.config['appName']} < Formula
  desc "{self.config['appName']}"
  homepage "{repo_url}"
  url "{repo_url}/releases/download/v{self.config['version']}/{self.config['appName']}-{self.config['version']}.tar.gz"
  version "{self.config['version']}"
  
  def install
    prefix.install Dir["./*"]
  end
end
"""

    def _write_formula(self, content: str) -> str:
        """Write formula to file."""
        formula_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName'].lower()}.rb"
        )

        with open(formula_path, 'w') as f:
            f.write(content)

        return formula_path
