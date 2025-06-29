#!/usr/bin/env python3
"""
Version information for MultiRing Strobo Disc Generator
Single source of truth for version management
"""

__version__ = "0.9.4"
__version_info__ = (0, 9, 4)

# Build metadata
__app_name__ = "MultiRing Strobo Disc Generator"
__package_name__ = "multiringstrobodiscgen"
__author__ = "Miguel Scaramozino"
__email__ = "mikele@gmail.com"
__description__ = "A handy tool for creating custom stroboscopic discs to check if your turntables are spinning at the right speed"
__license__ = "CC-BY-NC-SA-4.0"
__homepage__ = "https://github.com/mikelexp/multiringstrobodiscgen"

def get_version():
    """Get the version string"""
    return __version__

def get_version_info():
    """Get version as tuple (major, minor, patch)"""
    return __version_info__

def get_full_title():
    """Get full application title with version"""
    return f"{__app_name__} v{__version__}"

if __name__ == "__main__":
    print(__version__)