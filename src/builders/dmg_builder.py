from builders.base_builder import BaseBuilder
import subprocess
import os
import shutil

class DmgBuilder(BaseBuilder):
    def build(self) -> str:
        """Generate a .dmg installer."""
        self.logger.info(f"Creating .dmg installer for {self.config['appName']}")
        self.ensure_output_directory()

        dmg_path = os.path.join(
            self.config['outputDir'],
            f"{self.config['appName']}-{self.config['version']}.dmg"
        )

        temp_dir = self._prepare_temp_directory()
        try:
            self._create_dmg(dmg_path, temp_dir)
            return dmg_path
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _prepare_temp_directory(self) -> str:
        """Prepare temporary directory for DMG contents."""
        temp_dir = os.path.join(self.config['outputDir'], 'temp_dmg')
        os.makedirs(temp_dir, exist_ok=True)

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

        return temp_dir

    def _create_dmg(self, dmg_path: str, temp_dir: str) -> None:
        """Create DMG file using create-dmg."""
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

        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"Successfully created .dmg at {dmg_path}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create .dmg: {str(e)}")
            raise