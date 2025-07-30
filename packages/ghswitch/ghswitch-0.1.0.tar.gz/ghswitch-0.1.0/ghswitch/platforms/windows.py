"""
Windows-specific platform handler for GitHub Account Manager.
"""

import os
import subprocess
import base64
from pathlib import Path
from .base import BasePlatformHandler

class WindowsHandler(BasePlatformHandler):
    """Handler for Windows-specific operations."""
    
    def get_config_dir(self):
        """Get the directory where configuration files should be stored."""
        return Path(os.environ["USERPROFILE"]) / ".ghswitch"
    
    def get_ssh_dir(self):
        """Get the SSH directory."""
        return Path(os.environ["USERPROFILE"]) / ".ssh"
    
    def start_ssh_agent(self):
        """Start the SSH agent if it's not already running."""
        try:
            # Check if the SSH agent is running
            subprocess.run(
                "ssh-add -l",
                shell=True,
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            # Start the SSH agent
            subprocess.run(
                "start-ssh-agent.cmd",
                shell=True,
                check=False
            )
    
    def add_ssh_key_to_agent(self, key_path):
        """Add an SSH key to the SSH agent."""
        self.start_ssh_agent()
        try:
            self.run_command(f'ssh-add -D')  # Clear existing keys
            self.run_command(f'ssh-add "{key_path}"')
            return True
        except subprocess.CalledProcessError:
            return False
    
    def setup_credential_manager(self, account_name, token):
        """Store GitHub token in Windows Credential Manager."""
        if token:
            try:
                # Use cmdkey to store the token
                # Encode the token to avoid command line issues
                encoded_token = base64.b64encode(token.encode()).decode()
                self.run_command(
                    f'cmdkey /generic:ghswitch-{account_name} /user:GitHub /pass:{encoded_token}'
                )
                return True
            except subprocess.CalledProcessError:
                return False
        return False
    
    def get_token_from_credential_manager(self, account_name):
        """Retrieve GitHub token from Windows Credential Manager."""
        # This is tricky in Windows as cmdkey doesn't have a way to retrieve passwords
        # We'll store the encoded token in the config file instead
        return None
