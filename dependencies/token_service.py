import os
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWEInvalidAuth
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
secret = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_tokens(data: dict):
    data_encode = data.copy()
    current_time = datetime.now(timezone.utc)    
    data_encode.update({
        "exp": int((current_time + timedelta(hours=1)).replace(tzinfo=timezone.utc).timestamp()), # expiration time
        "iat": int(current_time.replace(tzinfo=timezone.utc).timestamp()), # issued at time (current time)
    })
    access_token = jwt.encode(
        data_encode, 
        secret,
        ALGORITHM,
    )

    data_encode.update({
        "exp": int((current_time + timedelta(days=1)).replace(tzinfo=timezone.utc).timestamp()), # expiration time
        "iat": int(current_time.replace(tzinfo=timezone.utc).timestamp()), # issued at time (current time)
    })
    refresh_token = jwt.encode(
        data_encode,
        secret,
        ALGORITHM
    )
    return access_token, refresh_token
    
def check_token(token):
    if not token:
        return JWEInvalidAuth
    try:
        decoded = jwt.decode(
            token, 
            secret, 
            algorithms=[ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True
            }
        )
        return decoded
    except ExpiredSignatureError as e:
        print(f"Token expired: {str(e)}")
        return ExpiredSignatureError
    except JWEInvalidAuth as k:
        print(f"Invalid token: {str(k)}")
        return JWEInvalidAuth