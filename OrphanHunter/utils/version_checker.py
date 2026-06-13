"""Version checker for OrphanHunter updates."""
import urllib.request
import json
from typing import Tuple, Optional
from packaging import version


class VersionChecker:
    """Check for OrphanHunter updates on GitHub."""
    
    GITHUB_API_URL = "https://api.github.com/repos/Hazardous-God/orphanhunter/releases/latest"
    CURRENT_VERSION = "1.3"
    
    def __init__(self):
        """Initialize version checker."""
        self.latest_version = None
        self.release_notes = None
        self.release_url = None
    
    def check_for_updates(self, timeout: int = 5) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check for updates on GitHub.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (update_available: bool, version: str, message: str)
        """
        try:
            # Make request to GitHub API
            req = urllib.request.Request(
                self.GITHUB_API_URL,
                headers={'User-Agent': 'OrphanHunter-UpdateChecker'}
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode())
            
            # Parse release data
            self.latest_version = data.get('tag_name', '').lstrip('v')
            self.release_notes = data.get('body', '')
            self.release_url = data.get('html_url', '')
            
            # Compare versions
            if self.latest_version:
                try:
                    current = version.parse(self.CURRENT_VERSION)
                    latest = version.parse(self.latest_version)
                    
                    if latest > current:
                        message = (
                            f"Update available: v{self.latest_version}\n"
                            f"Current version: v{self.CURRENT_VERSION}\n\n"
                            f"Visit: {self.release_url}"
                        )
                        return True, self.latest_version, message
                    else:
                        return False, self.latest_version, "You're running the latest version!"
                
                except Exception as e:
                    return False, None, f"Error comparing versions: {e}"
            else:
                return False, None, "Could not determine latest version"
        
        except urllib.error.URLError as e:
            return False, None, f"Network error: Unable to check for updates"
        except json.JSONDecodeError:
            return False, None, "Error parsing GitHub response"
        except Exception as e:
            return False, None, f"Error checking for updates: {e}"
    
    def get_release_notes(self) -> str:
        """Get release notes for the latest version.
        
        Returns:
            Release notes text
        """
        return self.release_notes or "No release notes available"
    
    def get_current_version(self) -> str:
        """Get current version string.
        
        Returns:
            Current version
        """
        return self.CURRENT_VERSION


