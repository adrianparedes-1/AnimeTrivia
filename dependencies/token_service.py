import os, redis
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWEInvalidAuth
from fastapi import Response, status
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
secret = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_tokens(data: dict):
    data_encode = data.copy()
    current_time = datetime.now(timezone.utc)    
    data_encode.update({
        "exp": int((current_time + timedelta(hours=1)).replace(tzinfo=timezone.utc).timestamp()), # expiration time for app access token
        "iat": int(current_time.replace(tzinfo=timezone.utc).timestamp()), # issued at time (current time)
    })
    access_token = jwt.encode(
        data_encode, 
        secret,
        ALGORITHM,
    )

    data_encode.update({
        "exp": int((current_time + timedelta(days=1)).replace(tzinfo=timezone.utc).timestamp()), # expiration time for app refresh token
        "iat": int(current_time.replace(tzinfo=timezone.utc).timestamp()), # issued at time (current time)
    })
    
    refresh_token = jwt.encode(
        data_encode,
        secret,
        ALGORITHM
    )
    return access_token, refresh_token
    
def check_token(token, r) -> dict:
    """
    This function check jwt token passed in the request's headers, and verifies it with the session in redis.
    If it is valid, it returns a decoded token.
    
    """
    
    if not token:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        
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

        r_token = r.get(f"{decoded['username']}:app_access_token")
        if not r_token or token != r_token:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return decoded  # Return the decoded dict directly
    

    # TODO: remove dependency on fastapi from this service. I will need to adjust validation logic in middleware as well btw.

    except ExpiredSignatureError as e:
        print(f"Token expired: {str(e)}")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWEInvalidAuth as k:
        print(f"Invalid token: {str(k)}")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)