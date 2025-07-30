"""
Talwar - AI-powered web application security testing tool
"""

__version__ = "0.1.1"

from .agent import Agent
from .run import main
from .license import LicenseManager

# Initialize license manager
LICENSE_MANAGER = LicenseManager(api_key="your_api_key_here")

def check_license():
    """Check if a valid license exists"""
    if not LICENSE_MANAGER.check_license():
        raise LicenseError(
            "No valid license found. Please purchase a license at https://talwar.ai/pricing"
        )

class LicenseError(Exception):
    """Exception raised when license validation fails"""
    pass

__all__ = ['Agent', 'main'] 