from config.config_loader import ConfigLoader
from utils.logger import Logger
from builders.pkg_builder import PkgBuilder
from builders.dmg_builder import DmgBuilder
from services.validator import InstallerValidator
from services.homebrew import HomebrewFormulaGenerator

def main():
    """Main execution function."""
    try:
        # Setup logger
        logger = Logger.setup()

        # Load configuration
        config = ConfigLoader.load('InstallerConfig.json')

        # Initialize builders and services
        pkg_builder = PkgBuilder(config, logger)
        dmg_builder = DmgBuilder(config, logger)
        validator = InstallerValidator(logger)
        homebrew_generator = HomebrewFormulaGenerator(config, logger)

        # Create installers
        pkg_path = pkg_builder.build()
        dmg_path = dmg_builder.build()

        # Validate installers
        macos_versions = ['Ventura', 'Sonoma', 'Sequoia']
        validator.validate(pkg_path, macos_versions)
        validator.validate(dmg_path, macos_versions)

        # Generate Homebrew formula
        homebrew_generator.generate('https://github.com/example/app')

    except Exception as e:
        logger.error(f"Build process failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()