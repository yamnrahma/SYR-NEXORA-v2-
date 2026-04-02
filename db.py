import json
import os

def load_vulnerability_db(file_path="vulns.json"):
    if not os.path.exists(file_path):
        default_db = {
            "21": {"service": "FTP", "risk": "Cleartext creds", "severity": "High"},
            "22": {"service": "SSH", "risk": "Brute force target", "severity": "Medium"},
            "80": {"service": "HTTP", "risk": "Outdated server", "severity": "Medium"},
            "443": {"service": "HTTPS", "risk": "SSL/TLS Vulns", "severity": "Low"}
        }
        with open(file_path, 'w') as f:
            json.dump(default_db, f, indent=4)
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        return {int(k): v for k, v in data.items()}

vuln_db = load_vulnerability_db()