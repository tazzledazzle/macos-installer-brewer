from builders.base_builder import BaseBuilder
import subprocess
import os

class PkgBuilder(BaseBuilder):
    def build(self) -> str:
        """Generate a .pkg installer."""
        self.logger.info(f"Creating .pkg installer for {self.config['appName']}")
        self.ensure_output_directory()

        pkg_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName']}-{self.config['version']}.pkg"
        )

        cmd = [
            'pkgbuild',
            '--root', './app',
            '--identifier', self.config['identifier'],
            '--version', self.config['version'],
            '--install-location', f"/Applications/{self.config['appName']}.app",
            '--scripts', './scripts',
            pkg_path
        ]

        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"Successfully created .pkg at {pkg_path}")
            return pkg_path
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create .pkg: {str(e)}")
            raise