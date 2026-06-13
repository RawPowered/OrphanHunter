# OrphanHunter Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3] - 2025-10-16

### Added
- **Self-Migration System**: OrphanHunter can now migrate itself into a `.ORPHANHUNTER` folder within your project root
  - Keeps all OrphanHunter files, reports, and backups organized in one place
  - Doesn't interfere with your project's file structure
  - Optional migration prompt on first run with v1.3
  - Manual migration button in Configuration tab
  - Migration status tracking to avoid re-prompting

- **Manual SQL Credentials UI**: New dedicated dialog for database configuration
  - Parse credentials from config.php automatically
  - Edit and test connections before saving
  - Credentials stored in OrphanHunter config (not config.php)
  - No more relying on monolithic config files
  - "Configure SQL Connection" button in Configuration tab

- **GitHub Version Checking**: Stay up to date with the latest releases
  - "Check for Updates" button in Configuration tab
  - Compares current version with latest GitHub release
  - Displays release notes and download link
  - One-time migration check on startup (doesn't re-check after passing)
  - Optional - respects user privacy

- **New Dependencies**: Added `packaging` library for version comparison

### Changed
- Renamed main script from `system-mapper.py` to `OrphanHunter.py`
- Updated version number to 1.3 across all files
- Modified database connection logic to use saved credentials instead of parsing config.php
- Application name updated to "OrphanHunter" throughout UI
- Live database connection now uses stored credentials by default

### Improved
- Better organization with `.ORPHANHUNTER` folder structure
- More reliable SQL connections with manual credential management
- User experience with guided migration process
- Update awareness with GitHub version checking

### Technical Details
- New files:
  - `OrphanHunter/operations/migration_manager.py` - Handles self-migration
  - `OrphanHunter/gui/sql_connection_dialog.py` - SQL credentials UI
  - `OrphanHunter/utils/version_checker.py` - GitHub version checking
  - `CHANGELOG.md` - This file!
  
- Modified files:
  - `OrphanHunter/__init__.py` - Version bump to 1.3
  - `OrphanHunter/utils/config.py` - New config fields for migration and SQL
  - `OrphanHunter/analyzer/live_db_connector.py` - Support for saved credentials
  - `OrphanHunter/gui/main_window.py` - Migration prompt, SQL dialog, version check
  - `README.md` - Updated for v1.3 features

---

## [1.2] - 2025-10-14

### Added
- **URL Migration Tool**: Revolutionary 7-step workflow for converting hardcoded URLs to dynamic references
  - Intelligent detection of hardcoded URLs across PHP, HTML, JS, CSS, SQL
  - Smart classification (internal vs external URLs)
  - Multiple replacement formats (BASE_URL, safe_url(), asset_url(), custom)
  - Auto-detection from config.php
  - 2-pass verification system
  - Full backup and selective rollback capabilities
  
- **Enhanced CSS Analysis**: 
  - Conflict detection between stylesheets
  - Duplicate selector identification
  - CSS usage mapping per page
  - Style error report generation

- **Asset Analysis**:
  - Orphaned JS/TS/JSON/CSS detection
  - Import/export tracking for JavaScript modules
  - Reference counting for assets

### Improved
- Live database connection capabilities
- Dependency graph visualization
- Documentation generation
- Error handling and logging

### Technical
- Added URL analyzer module
- Enhanced CSS parser
- Improved reference tracking
- New markdown generators for reports

---

## [1.1] - 2025-10-10

### Added
- Live MySQL database connection support
- Config.php credential parsing
- Real-time database URL scanning
- Enhanced backup system

### Fixed
- File encoding detection issues
- Path normalization on Windows
- SQL parser edge cases

---

## [1.0] - 2025-10-01

### Initial Release
- Project scanning and file analysis
- Orphaned file detection
- PHP dependency parsing
- SQL dump analysis
- Safe deletion manager with rollback
- Backup creation and restoration
- Sitemap generation
- System documentation generation
- PyQt5 GUI interface
- Portable, auto-installing design

---

## Migration Notes

### Upgrading to v1.3

1. **First Run**: On first launch with v1.3, you'll be prompted to migrate to the new structure. This is optional but recommended.

2. **Manual Migration**: If you skip the prompt, you can manually migrate anytime via the "Migrate to v1.3 Structure" button in the Configuration tab.

3. **SQL Credentials**: If you were using live database connection in v1.2, you'll need to configure SQL credentials using the new "Configure SQL Connection" button. The auto-detect feature can pull credentials from your config.php.

4. **File Structure After Migration**:
   ```
   YourProject/
   ├── .ORPHANHUNTER/
   │   ├── OrphanHunter.py
   │   ├── cleanup.py
   │   ├── OrphanHunter/
   │   ├── backups/
   │   ├── reports/
   │   ├── *.md files
   │   └── system-mapper-config.json
   └── [your project files]
   ```

5. **Backward Compatibility**: The old `system-mapper.py` still exists for compatibility. Use `OrphanHunter.py` for the new version.

---

## Upgrade Checklist

- [ ] Backup your current OrphanHunter installation
- [ ] Run OrphanHunter v1.3
- [ ] Complete migration when prompted (or manually)
- [ ] Configure SQL credentials if using live database
- [ ] Verify all features work correctly
- [ ] Delete old files if migration successful

---

**For more information, see [README.md](README.md) and [URL-MIGRATION-TOOL.md](URL-MIGRATION-TOOL.md)**


