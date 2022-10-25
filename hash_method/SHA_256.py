import hashlib


def double_sha256(entropy):
    
    return hashlib.sha256(bytes.fromhex(hashlib.sha256(bytes.fromhex(entropy)).hexdigest())).hexdigest()