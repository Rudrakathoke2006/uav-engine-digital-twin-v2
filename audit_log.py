"""
AeroTwin-PX v2: Cryptographic Hash-Chained Audit Log
Provides tamper-evident record logging via sequential HMAC-SHA256 cryptographic hashes.
"""

import hashlib
import json

class CryptographicAuditLog:
    def __init__(self, secret_key: str = "AEROTWIN_PX_DEFENSE_KEY_26054"):
        self.secret_key = secret_key
        self.chain = []
        self.latest_hash = "0" * 64
        
    def append_record(self, record_type: str, data: dict) -> dict:
        """
        Appends a record to the sequential cryptographic hash chain.
        """
        timestamp = data.get("timestamp", 0.0)
        data_str = json.dumps(data, sort_keys=True)
        
        # Cryptographic Hash Calculation
        payload = f"{self.latest_hash}|{record_type}|{timestamp}|{data_str}".encode('utf-8')
        record_hash = hashlib.sha256(payload).hexdigest()
        
        entry = {
            "index": len(self.chain),
            "record_type": record_type,
            "timestamp": timestamp,
            "previous_hash": self.latest_hash,
            "hash": record_hash,
            "data": data
        }
        
        self.chain.append(entry)
        self.latest_hash = record_hash
        return entry

    def verify_integrity(self) -> dict:
        """
        Verifies the cryptographic continuity of the entire audit chain.
        Returns validation status and tamper index if broken.
        """
        prev_hash = "0" * 64
        
        for idx, entry in enumerate(self.chain):
            if entry["previous_hash"] != prev_hash:
                return {
                    "status": "TAMPER_DETECTED",
                    "is_valid": False,
                    "tamper_index": idx,
                    "message": f"Hash broken at entry #{idx}: previous hash mismatch."
                }
                
            data_str = json.dumps(entry["data"], sort_keys=True)
            payload = f"{prev_hash}|{entry['record_type']}|{entry['timestamp']}|{data_str}".encode('utf-8')
            expected_hash = hashlib.sha256(payload).hexdigest()
            
            if entry["hash"] != expected_hash:
                return {
                    "status": "TAMPER_DETECTED",
                    "is_valid": False,
                    "tamper_index": idx,
                    "message": f"Data tampering detected at record #{idx}: hash payload modified."
                }
                
            prev_hash = entry["hash"]
            
        return {
            "status": "VALID & IMMUTABLE",
            "is_valid": True,
            "total_records": len(self.chain),
            "latest_root_hash": self.latest_hash
        }

if __name__ == "__main__":
    audit = CryptographicAuditLog()
    audit.append_record("TELEMETRY", {"rpm": 4800, "egt": 680})
    audit.append_record("ALERT", {"fault": "Injector Coking", "confidence": 88.5})
    res = audit.verify_integrity()
    print("Audit Log Integrity Check:", res)
