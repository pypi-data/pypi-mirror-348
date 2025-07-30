"""
Base platform handler for GitHub Account Manager.
"""

import os
import subprocess
from pathlib import Path

class BasePlatformHandler:
    """Base class for platform-specific operations."""
    
    def get_config_dir(self):
        """Get the directory where configuration files should be stored."""
        return Path.home() / ".ghswitch"
    
    def ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        config_dir = self.get_config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def get_ssh_dir(self):
        """Get the SSH directory."""
        return Path.home() / ".ssh"
    
    def ensure_ssh_dir(self):
        """Ensure the SSH directory exists."""
        ssh_dir = self.get_ssh_dir()
        ssh_dir.mkdir(parents=True, exist_ok=True)
        return ssh_dir
    
    def run_command(self, command, cwd=None):
        """Run a shell command and return the output."""
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        return result.stdout.strip()
    
    def set_git_config(self, key, value, global_config=True, repo_path=None):
        """Set a Git configuration value."""
        scope = "--global" if global_config else "--local"
        cwd = repo_path if repo_path else None
        self.run_command(f'git config {scope} "{key}" "{value}"', cwd=cwd)
    
    def get_git_config(self, key, global_config=True, repo_path=None):
        """Get a Git configuration value."""
        scope = "--global" if global_config else "--local"
        cwd = repo_path if repo_path else None
        try:
            return self.run_command(f'git config {scope} "{key}"', cwd=cwd)
        except subprocess.CalledProcessError:
            return None
    
    def setup_ssh_config(self, account_name, ssh_key_path):
        """Set up SSH configuration for the account."""
        ssh_config_path = self.get_ssh_dir() / "config"
        
        # Create the config file if it doesn't exist
        if not ssh_config_path.exists():
            ssh_config_path.touch()
        
        # Check if the host entry already exists
        with open(ssh_config_path, 'r') as f:
            config_content = f.read()
        
        host_entry = f"Host github.com-{account_name}"
        
        if host_entry not in config_content:
            # Add the host entry
            with open(ssh_config_path, 'a') as f:
                f.write(f"\n{host_entry}\n")
                f.write(f"  HostName github.com\n")
                f.write(f"  User git\n")
                f.write(f"  IdentityFile {ssh_key_path}\n")
                f.write(f"  IdentitiesOnly yes\n\n")
        
        return f"github.com-{account_name}"
    
    def generate_ssh_key(self, account_name, email):
        """Generate a new SSH key for the account."""
        ssh_dir = self.ensure_ssh_dir()
        key_path = ssh_dir / f"id_rsa_{account_name}"
        
        # Generate the key if it doesn't exist
        if not key_path.exists():
            self.run_command(f'ssh-keygen -t rsa -b 4096 -C "{email}" -f "{key_path}" -N ""')
        
        return key_path
