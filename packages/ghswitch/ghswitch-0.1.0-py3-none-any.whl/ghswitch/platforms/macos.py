"""
macOS-specific platform handler for GitHub Account Manager.
"""

import os
import subprocess
from pathlib import Path
from .base import BasePlatformHandler

class MacOSHandler(BasePlatformHandler):
    """Handler for macOS-specific operations."""
    
    def start_ssh_agent(self):
        """Start the SSH agent if it's not already running."""
        try:
            # Check if SSH agent is running
            os.environ["SSH_AUTH_SOCK"]
        except KeyError:
            # Start SSH agent
            result = subprocess.run(
                "eval `ssh-agent -s` && echo $SSH_AUTH_SOCK",
                shell=True,
                text=True,
                capture_output=True
            )
            os.environ["SSH_AUTH_SOCK"] = result.stdout.strip()
    
    def add_ssh_key_to_agent(self, key_path):
        """Add an SSH key to the SSH agent."""
        self.start_ssh_agent()
        try:
            self.run_command(f'ssh-add -D')  # Clear existing keys
            self.run_command(f'ssh-add "{key_path}"')
            return True
        except subprocess.CalledProcessError:
            return False
    
    def setup_keychain(self, account_name, token):
        """Store GitHub token in macOS Keychain."""
        if token:
            try:
                # Store token in keychain
                self.run_command(
                    f'security add-generic-password -a "ghswitch-{account_name}" -s "GitHub Token" -w "{token}" -U'
                )
                return True
            except subprocess.CalledProcessError:
                return False
        return False
    
    def get_token_from_keychain(self, account_name):
        """Retrieve GitHub token from macOS Keychain."""
        try:
            token = self.run_command(
                f'security find-generic-password -a "ghswitch-{account_name}" -s "GitHub Token" -w'
            )
            return token
        except subprocess.CalledProcessError:
            return None
