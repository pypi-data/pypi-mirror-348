"""
Configuration management for GitHub Account Manager.
"""

import os
import yaml
from pathlib import Path
from ghswitch.platforms import get_platform_handler

class Config:
    """Configuration manager for GitHub Account Manager."""
    
    def __init__(self):
        self.platform = get_platform_handler()
        self.config_dir = self.platform.ensure_config_dir()
        self.config_file = self.config_dir / "config.yaml"
        self.repo_config_file = ".github-account"
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file."""
        if not self.config_file.exists():
            return {
                "accounts": {},
                "primary": None,
                "version": 1
            }
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def add_account(self, name, username, email, ssh_key=None, token=None, generate_key=False):
        """
        Add a new GitHub account.
        
        Args:
            name: A unique name for the account
            username: GitHub username
            email: Email associated with the GitHub account
            ssh_key: Path to SSH key (optional)
            token: GitHub personal access token (optional)
            generate_key: Whether to generate a new SSH key if none is provided
        
        Returns:
            bool: True if successful, False otherwise
        """
        if name in self.config["accounts"]:
            return False, f"Account '{name}' already exists"
        
        # Handle SSH key
        if ssh_key:
            ssh_key_path = Path(ssh_key).expanduser().resolve()
            if not ssh_key_path.exists():
                return False, f"SSH key '{ssh_key}' does not exist"
        elif generate_key:
            ssh_key_path = self.platform.generate_ssh_key(name, email)
        else:
            ssh_key_path = None
        
        # Set up SSH config if we have a key
        ssh_host = None
        if ssh_key_path:
            ssh_host = self.platform.setup_ssh_config(name, ssh_key_path)
        
        # Store token in platform-specific secure storage
        if token:
            if hasattr(self.platform, "setup_keychain"):
                self.platform.setup_keychain(name, token)
            elif hasattr(self.platform, "setup_credential_manager"):
                self.platform.setup_credential_manager(name, token)
        
        # Add account to config
        self.config["accounts"][name] = {
            "username": username,
            "email": email,
            "ssh_key": str(ssh_key_path) if ssh_key_path else None,
            "ssh_host": ssh_host,
            "token_stored": bool(token)
        }
        
        # Set as primary if it's the first account
        if not self.config["primary"]:
            self.config["primary"] = name
        
        self._save_config()
        return True, f"Account '{name}' added successfully"
    
    def remove_account(self, name):
        """Remove a GitHub account."""
        if name not in self.config["accounts"]:
            return False, f"Account '{name}' does not exist"
        
        # Remove from config
        del self.config["accounts"][name]
        
        # Update primary if needed
        if self.config["primary"] == name:
            if self.config["accounts"]:
                self.config["primary"] = next(iter(self.config["accounts"]))
            else:
                self.config["primary"] = None
        
        self._save_config()
        return True, f"Account '{name}' removed successfully"
    
    def set_primary(self, name):
        """Set the primary GitHub account."""
        if name not in self.config["accounts"]:
            return False, f"Account '{name}' does not exist"
        
        self.config["primary"] = name
        self._save_config()
        return True, f"Account '{name}' set as primary"
    
    def get_accounts(self):
        """Get all configured accounts."""
        return self.config["accounts"]
    
    def get_account(self, name):
        """Get a specific account by name."""
        return self.config["accounts"].get(name)
    
    def get_primary(self):
        """Get the primary account."""
        if not self.config["primary"]:
            return None
        return self.get_account(self.config["primary"])
    
    def get_primary_name(self):
        """Get the name of the primary account."""
        return self.config["primary"]
    
    def get_repo_account(self, repo_path=None):
        """Get the account configured for a repository."""
        if not repo_path:
            repo_path = os.getcwd()
        
        repo_config_path = Path(repo_path) / self.repo_config_file
        if repo_config_path.exists():
            with open(repo_config_path, 'r') as f:
                account_name = f.read().strip()
                if account_name in self.config["accounts"]:
                    return account_name, self.get_account(account_name)
        
        return self.config["primary"], self.get_primary()
    
    def set_repo_account(self, name, repo_path=None):
        """Set the account for a repository."""
        if name not in self.config["accounts"]:
            return False, f"Account '{name}' does not exist"
        
        if not repo_path:
            repo_path = os.getcwd()
        
        # Check if it's a git repository
        git_dir = Path(repo_path) / ".git"
        if not git_dir.exists():
            return False, f"'{repo_path}' is not a git repository"
        
        repo_config_path = Path(repo_path) / self.repo_config_file
        with open(repo_config_path, 'w') as f:
            f.write(name)
        
        return True, f"Account '{name}' set for repository at '{repo_path}'"
