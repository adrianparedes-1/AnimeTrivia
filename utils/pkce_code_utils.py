import secrets, base64, hashlib

def code_verifier() -> bytes:
    code = secrets.token_bytes(64)
    return code

def code_hashing(code: bytes) -> bytes:
    code_challenge = hashlib.sha256(code).digest()
    return code_challenge

def code_encoder(code_challenge: bytes) -> bytes:
    return base64.urlsafe_b64encode(code_challenge)
