"""
Platform-specific implementations for GitHub Account Manager.
"""

import platform
import importlib

def get_platform_handler():
    """
    Returns the appropriate platform handler based on the current operating system.
    """
    system = platform.system().lower()
    
    if system == "darwin":
        module = importlib.import_module("ghswitch.platforms.macos")
        return module.MacOSHandler()
    elif system == "windows":
        module = importlib.import_module("ghswitch.platforms.windows")
        return module.WindowsHandler()
    else:
        # Default to a basic handler for other platforms
        from ghswitch.platforms.base import BasePlatformHandler
        return BasePlatformHandler()
