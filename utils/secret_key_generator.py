import secrets
import base64
from pathlib import Path

env_path = Path("../.env")
env_key = "SECRET_KEY"

if env_path.exists():
    content = env_path.read_text()
    if env_key in content:
        exit()

key = secrets.token_bytes(32)
encoded_key = base64.urlsafe_b64encode(key).decode()

with open(env_path, "a") as f:
    f.write(f"{env_key}={encoded_key}\n")