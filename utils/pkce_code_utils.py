import secrets, base64, hashlib

def code_verifier() -> str:
    code = secrets.token_urlsafe(64)
    return code

def code_challenge(verifier: str) -> str:
    code_hash = code_hashing(verifier)
    return code_encoder(code_hash)

def code_hashing(code: str) -> bytes:
    code_encoded = code.encode("utf-8")
    code_challenge = hashlib.sha256(code_encoded).digest()
    return code_challenge

def code_encoder(code_challenge: bytes) -> bytes:
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode("utf-8")
