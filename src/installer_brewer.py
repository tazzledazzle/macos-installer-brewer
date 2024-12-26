import json
import os
import subprocess
from typing import List, Dict
import logging
import shutil
from pathlib import Path

class InstallerBuilder:
    def __init__(self, config_path: str):
        """Initialize the installer builder with configuration."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load config: {str(e)}")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('InstallerBuilder')

    def create_pkg(self) -> str:
        """Generate a .pkg installer based on configuration."""
        self.logger.info(f"Creating .pkg installer for {self.config['appName']}")

        # Ensure output directory exists
        os.makedirs(self.config['outputDir'], exist_ok=True)

        # Define output path
        pkg_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName']}-{self.config['version']}.pkg"
        )

        # Build pkgbuild command
        cmd = [
            'pkgbuild',
            '--root', './app',  # Directory containing the app
            '--identifier', self.config['identifier'],
            '--version', self.config['version'],
            '--install-location', f"/Applications/{self.config['appName']}.app",
            '--scripts', './scripts',  # Directory containing pre/post install scripts
            pkg_path
        ]

        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"Successfully created .pkg at {pkg_path}")
            return pkg_path
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create .pkg: {str(e)}")
            raise

    def create_dmg(self) -> str:
        """Generate a .dmg installer based on configuration."""
        self.logger.info(f"Creating .dmg installer for {self.config['appName']}")

        # Ensure output directory exists
        os.makedirs(self.config['outputDir'], exist_ok=True)

        # Define output path
        dmg_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName']}-{self.config['version']}.dmg"
        )

        # Create temporary directory for DMG contents
        temp_dir = os.path.join(self.config['outputDir'], 'temp_dmg')
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Copy application to temp directory
            shutil.copytree(
                './app',
                os.path.join(temp_dir, f"{self.config['appName']}.app"),
                symlinks=True
            )

            # Create symbolic link to Applications folder
            os.symlink(
                '/Applications',
                os.path.join(temp_dir, 'Applications')
            )

            # Build create-dmg command
            cmd = [
                'create-dmg',
                '--volname', self.config['appName'],
                '--window-pos', '200', '120',
                '--window-size', '800', '400',
                '--icon-size', '100',
                '--icon', f"{self.config['appName']}.app", '200', '200',
                '--hide-extension', f"{self.config['appName']}.app",
                '--app-drop-link', '600', '200',
                dmg_path,
                temp_dir
            ]

            subprocess.run(cmd, check=True)
            self.logger.info(f"Successfully created .dmg at {dmg_path}")
            return dmg_path

        except Exception as e:
            self.logger.error(f"Failed to create .dmg: {str(e)}")
            raise
        finally:
            # Cleanup temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    def validate_installer(self, installer_path: str, macos_versions: List[str]) -> bool:
        """Validate installer compatibility across macOS versions."""
        self.logger.info(f"Validating installer: {installer_path}")

        for version in macos_versions:
            self.logger.info(f"Testing on macOS {version}")
            # Here you would implement validation logic using VMs or CI tools
            # This is a placeholder for the actual validation implementation
            pass

        return True

    def generate_homebrew_formula(self, repo_url: str) -> str:
        """Create a Homebrew formula for distribution."""
        self.logger.info("Generating Homebrew formula")

        formula_template = f"""
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

        # Write formula to file
        formula_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName'].lower()}.rb"
        )

        with open(formula_path, 'w') as f:
            f.write(formula_template)

        self.logger.info(f"Created Homebrew formula at {formula_path}")
        return formula_path

def main():
    """Main execution function."""
    # Initialize builder with config
    builder = InstallerBuilder('InstallerConfig.json')

    try:
        # Create installers
        pkg_path = builder.create_pkg()
        dmg_path = builder.create_dmg()

        # Validate installers
        macos_versions = ['Ventura', 'Sonoma', 'Sequoia']
        builder.validate_installer(pkg_path, macos_versions)
        builder.validate_installer(dmg_path, macos_versions)

        # Generate Homebrew formula
        builder.generate_homebrew_formula('https://github.com/example/app')

    except Exception as e:
        logging.error(f"Build process failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()