import hashlib
import json
import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class LicenseManager:
    def __init__(self, api_key: str, package_name: str = "talwar"):
        self.api_key = api_key
        self.package_name = package_name
        self.license_file = os.path.expanduser("~/.talwar/license.json")
        self._ensure_license_dir()
        
    def _ensure_license_dir(self):
        """Ensure the license directory exists"""
        os.makedirs(os.path.dirname(self.license_file), exist_ok=True)
        
    def validate_license(self, license_key: str) -> bool:
        """Validate a license key with the license server"""
        try:
            response = requests.post(
                "https://api.talwar.ai/v1/validate-license",
                json={
                    "license_key": license_key,
                    "package_name": self.package_name,
                    "api_key": self.api_key
                }
            )
            if response.status_code == 200:
                data = response.json()
                self._save_license_data(data)
                return True
            return False
        except Exception:
            return False
            
    def _save_license_data(self, data: Dict[str, Any]):
        """Save license data to local file"""
        with open(self.license_file, 'w') as f:
            json.dump(data, f)
            
    def check_license(self) -> bool:
        """Check if a valid license exists"""
        try:
            if not os.path.exists(self.license_file):
                return False
                
            with open(self.license_file, 'r') as f:
                data = json.load(f)
                
            # Check if license is expired
            if datetime.fromisoformat(data['expires_at']) < datetime.now():
                return False
                
            # Verify license hash
            expected_hash = hashlib.sha256(
                f"{data['license_key']}{self.api_key}".encode()
            ).hexdigest()
            
            return data['hash'] == expected_hash
            
        except Exception:
            return False
            
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """Get current license information"""
        try:
            if not os.path.exists(self.license_file):
                return None
                
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None 