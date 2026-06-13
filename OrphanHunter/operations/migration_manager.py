"""Self-migration manager for OrphanHunter v1.3+."""
import shutil
from pathlib import Path
from typing import Tuple, List
import json


class MigrationManager:
    """Manages self-migration to .ORPHANHUNTER folder."""
    
    def __init__(self, project_root: Path):
        """Initialize migration manager.
        
        Args:
            project_root: Root directory of the project being analyzed
        """
        self.project_root = Path(project_root)
        self.orphanhunter_dir = self.project_root / '.ORPHANHUNTER'
        self.script_dir = Path(__file__).parent.parent.parent  # OrphanHunter repo root
        
    def is_migrated(self) -> bool:
        """Check if migration has already been completed."""
        marker_file = self.orphanhunter_dir / '.migration_complete'
        return marker_file.exists()
    
    def should_prompt_migration(self, config: dict) -> bool:
        """Check if we should prompt user for migration.
        
        Args:
            config: Application configuration dictionary
            
        Returns:
            True if should prompt, False otherwise
        """
        # Don't prompt if already migrated
        if config.get('migration_complete', False):
            return False
        
        # Don't prompt if user dismissed it
        if config.get('migration_dismissed', False):
            return False
        
        # Only prompt if project root is set
        if not self.project_root or not self.project_root.exists():
            return False
        
        return True
    
    def get_files_to_migrate(self) -> List[Tuple[Path, Path]]:
        """Get list of files to migrate.
        
        Returns:
            List of (source, destination) tuples
        """
        files = []
        
        # Main script (renamed)
        main_script = self.script_dir / 'OrphanHunter.py'
        if not main_script.exists():
            # Try old name
            main_script = self.script_dir / 'system-mapper.py'
        if main_script.exists():
            files.append((main_script, self.orphanhunter_dir / 'OrphanHunter.py'))
        
        # Cleanup script
        cleanup_script = self.script_dir / 'cleanup.py'
        if cleanup_script.exists():
            files.append((cleanup_script, self.orphanhunter_dir / 'cleanup.py'))
        
        # OrphanHunter package directory
        package_dir = self.script_dir / 'OrphanHunter'
        if package_dir.exists():
            files.append((package_dir, self.orphanhunter_dir / 'OrphanHunter'))
        
        # Documentation files
        for md_file in self.script_dir.glob('*.md'):
            # Skip git-specific docs
            if md_file.name.upper() not in ['GITHUB-SOCIAL-PREVIEW.MD', 'GITHUB-UPDATE-GUIDE.MD']:
                files.append((md_file, self.orphanhunter_dir / md_file.name))
        
        # Assets folder if exists
        assets_dir = self.script_dir / 'assets'
        if assets_dir.exists():
            files.append((assets_dir, self.orphanhunter_dir / 'assets'))
        
        return files
    
    def perform_migration(self, progress_callback=None) -> Tuple[bool, str, List[str]]:
        """Perform the migration.
        
        Args:
            progress_callback: Optional callback function(message: str)
            
        Returns:
            Tuple of (success: bool, message: str, errors: List[str])
        """
        errors = []
        
        try:
            # Create .ORPHANHUNTER directory
            if progress_callback:
                progress_callback("Creating .ORPHANHUNTER directory...")
            
            self.orphanhunter_dir.mkdir(exist_ok=True)
            
            # Get files to migrate
            files_to_migrate = self.get_files_to_migrate()
            
            if not files_to_migrate:
                return False, "No files found to migrate", ["Script directory not found"]
            
            # Copy files
            for i, (source, dest) in enumerate(files_to_migrate):
                if progress_callback:
                    progress_callback(f"Copying {source.name}... ({i+1}/{len(files_to_migrate)})")
                
                try:
                    if source.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(source, dest)
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
                except Exception as e:
                    errors.append(f"Error copying {source.name}: {e}")
            
            # Create subdirectories for generated content
            if progress_callback:
                progress_callback("Creating subdirectories...")
            
            (self.orphanhunter_dir / 'backups').mkdir(exist_ok=True)
            (self.orphanhunter_dir / 'reports').mkdir(exist_ok=True)
            
            # Create migration marker
            marker_file = self.orphanhunter_dir / '.migration_complete'
            marker_data = {
                'version': '1.3',
                'migrated_from': str(self.script_dir),
                'files_migrated': len(files_to_migrate) - len(errors)
            }
            
            with open(marker_file, 'w', encoding='utf-8') as f:
                json.dump(marker_data, f, indent=2)
            
            if progress_callback:
                progress_callback("Migration complete!")
            
            if errors:
                return True, f"Migration completed with {len(errors)} errors", errors
            else:
                return True, "Migration completed successfully!", []
                
        except Exception as e:
            return False, f"Migration failed: {e}", [str(e)]
    
    def get_migrated_paths(self) -> dict:
        """Get paths after migration.
        
        Returns:
            Dictionary with updated paths
        """
        return {
            'orphanhunter_root': str(self.orphanhunter_dir),
            'config_file': str(self.orphanhunter_dir / 'system-mapper-config.json'),
            'backup_directory': str(self.orphanhunter_dir / 'backups'),
            'reports_directory': str(self.orphanhunter_dir / 'reports')
        }


