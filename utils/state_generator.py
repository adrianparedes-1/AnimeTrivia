import secrets
import base64


def create_state() -> bytes:
    key = secrets.token_bytes(64)
    return key



# encoded_key = base64.urlsafe_b64encode(key)
