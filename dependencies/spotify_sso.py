from fastapi_sso import OpenID
from starlette.requests import Request
from fastapi_sso.sso.spotify import SpotifySSO
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SERVICE")
redirect_uri = os.getenv("CALLBACK_URL")

class CustomSpotifySSO(SpotifySSO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._custom_access_token: Optional[str] = None
        self._custom_refresh_token: Optional[str] = None
        self._custom_expires_in: Optional[int] = None
        self._custom_scope: Optional[str] = None
        self._generated_state: Optional[str] = None
        self.requires_state = True

    async def verify_and_process(self, request: Request) -> OpenID:
        user = await super().verify_and_process(request)
        token_data = self._oauth_client.token
        self._custom_access_token = token_data.get("access_token")
        self._custom_refresh_token = token_data.get("refresh_token")
        self._custom_expires_in = token_data.get("expires_in")
        self._custom_scope = token_data.get("scope")
        
        return user
    
# def sso_dependency() -> CustomSpotifySSO:
#     return CustomSpotifySSO (
#         client_id=client_id,
#         client_secret=client_secret,
#         redirect_uri=redirect_uri,
#         scope="user-read-email user-read-private"
#     )