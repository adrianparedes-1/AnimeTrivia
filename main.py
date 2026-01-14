import fnmatch, redis
from fastapi import FastAPI, APIRouter, Request, Response
from starlette.middleware.cors import CORSMiddleware
from dependencies.token_service import check_token
from dependencies.admin import admin
from modules.anime.routers import (
    anime_router
)
from modules.game.routers import game_router
from modules.user.routers import auth_router
from modules.menu.routers import (
    menu_router,
    profile_router
)

r = redis.Redis(host='localhost', port=6379, decode_responses=True) # middleware oauth flow
app = FastAPI()
admin.mount_to(app)
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router.router)
app.include_router(menu_router.router)
app.include_router(profile_router.router)
app.include_router(anime_router.router)
app.include_router(game_router.router)

@app.middleware("http")
async def auth_user(request: Request, call_next):
    public_paths = ["/favicon.ico", "/auth", "/auth/callback*", "/admin*", "/docs*", "/openapi.json"]

    if request.method == "OPTIONS":
        return await call_next(request)
    # print("Print request in middleware: " + (await request.json()))
    # if the path we are trying to access is a public path, go on to the route
    if any(fnmatch.fnmatch(request.url.path, pat) for pat in public_paths):
        return await call_next(request)
    
    """
    equivalent to:
    
    match_found = False
    for pat in public_paths:
        if fnmatch.fnmatch(request.url.path, pat):
            match_found = True
            break

    if match_found:
        return await call_next(request)
    """

    # otherwise, get the token from the header and validate it
    token = request.headers.get("authorization")
    # print(request.headers)
    response = check_token(token, r)
    
    # if the token validation is not successful, return the response from check_token which contains the error in the form of a Response object
    if isinstance(response, Response): 
        return response

    # if the token validation is successful (200 OK), then go on to the route and pass the decoded token (response)
    request.state.user = response
    return await call_next(request)
