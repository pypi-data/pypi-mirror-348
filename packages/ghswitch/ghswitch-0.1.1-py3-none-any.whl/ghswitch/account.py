"""
Account management for GitHub Account Manager.
"""

import os
import subprocess
from pathlib import Path
from ghswitch.config import Config
from ghswitch.platforms import get_platform_handler

class AccountManager:
    """Manager for GitHub accounts."""
    
    def __init__(self):
        self.config = Config()
        self.platform = get_platform_handler()
    
    def add_account(self, name, username, email, ssh_key=None, token=None, generate_key=False):
        """Add a new GitHub account."""
        return self.config.add_account(name, username, email, ssh_key, token, generate_key)
    
    def remove_account(self, name):
        """Remove a GitHub account."""
        return self.config.remove_account(name)
    
    def set_primary(self, name):
        """Set the primary GitHub account."""
        return self.config.set_primary(name)
    
    def list_accounts(self):
        """List all configured accounts."""
        accounts = self.config.get_accounts()
        primary = self.config.get_primary_name()
        
        result = []
        for name, account in accounts.items():
            is_primary = name == primary
            result.append({
                "name": name,
                "username": account["username"],
                "email": account["email"],
                "ssh_key": account["ssh_key"],
                "is_primary": is_primary
            })
        
        return result
    
    def use_account(self, name, global_config=False, repo_path=None):
        """
        Use a specific GitHub account.
        
        Args:
            name: Name of the account to use
            global_config: Whether to set as the global Git config
            repo_path: Path to the repository (if not global)
        
        Returns:
            tuple: (success, message)
        """
        account = self.config.get_account(name)
        if not account:
            return False, f"Account '{name}' does not exist"
        
        # If not global, ensure it's a git repository
        if not global_config:
            if not repo_path:
                repo_path = os.getcwd()
            
            git_dir = Path(repo_path) / ".git"
            if not git_dir.exists():
                return False, f"'{repo_path}' is not a git repository"
            
            # Set the account for this repository
            success, message = self.config.set_repo_account(name, repo_path)
            if not success:
                return success, message
        
        # Update Git configuration
        self.platform.set_git_config("user.name", account["username"], global_config, repo_path)
        self.platform.set_git_config("user.email", account["email"], global_config, repo_path)
        
        # Handle SSH key if available
        if account["ssh_key"]:
            ssh_key_path = Path(account["ssh_key"])
            
            # Add to SSH agent
            if hasattr(self.platform, "add_ssh_key_to_agent"):
                self.platform.add_ssh_key_to_agent(ssh_key_path)
            
            # Update Git SSH command if using a custom host
            if account["ssh_host"]:
                git_ssh_command = f'ssh -i {ssh_key_path} -F {self.platform.get_ssh_dir() / "config"}'
                self.platform.set_git_config("core.sshCommand", git_ssh_command, global_config, repo_path)
        
        # Set up remote URL if this is a repository
        if not global_config and account["ssh_host"]:
            try:
                # Get the current remote URL
                remote_url = self.platform.run_command("git remote get-url origin", cwd=repo_path)
                
                # If it's a GitHub URL, update it to use the SSH host
                if "github.com" in remote_url:
                    if remote_url.startswith("https://"):
                        # Convert HTTPS to SSH
                        new_url = remote_url.replace("https://github.com/", f"git@{account['ssh_host']}:")
                        self.platform.run_command(f'git remote set-url origin "{new_url}"', cwd=repo_path)
                    elif remote_url.startswith("git@github.com:"):
                        # Update SSH host
                        new_url = remote_url.replace("git@github.com:", f"git@{account['ssh_host']}:")
                        self.platform.run_command(f'git remote set-url origin "{new_url}"', cwd=repo_path)
            except subprocess.CalledProcessError:
                # Repository might not have a remote yet, that's okay
                pass
        
        if global_config:
            return True, f"Switched to account '{name}' globally"
        else:
            return True, f"Switched to account '{name}' for repository at '{repo_path}'"
    
    def get_current_account(self, repo_path=None):
        """Get the current account being used."""
        if not repo_path:
            repo_path = os.getcwd()
        
        try:
            # Check if it's a git repository
            git_dir = Path(repo_path) / ".git"
            if not git_dir.exists():
                name = self.config.get_primary_name()
                return name, self.config.get_account(name)
            
            # Get the account configured for this repository
            return self.config.get_repo_account(repo_path)
        except Exception:
            # Fall back to primary account
            name = self.config.get_primary_name()
            return name, self.config.get_account(name)
