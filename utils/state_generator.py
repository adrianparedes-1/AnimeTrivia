import secrets


def create_state() -> str:
    return secrets.token_urlsafe(64)

