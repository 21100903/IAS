import hashlib

def compute_sha256(data: bytes) -> str:
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def verify_sha256(data: bytes, expected_hash: str) -> bool:
    return compute_sha256(data) == expected_hash
