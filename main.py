from fastapi import FastAPI, APIRouter, Request, status
from starlette.middleware.cors import CORSMiddleware
from modules.user.routers import auth_router
from modules.menu.routers import menu_router
from dependencies.token_service import check_token

app = FastAPI()
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

@app.middleware("http")
async def auth_user(request: Request, call_next):
    public_paths = ["/auth", "/docs", "/openapi.json"]

    if request.method == "OPTIONS":
        return await call_next(request)
    
    # if the path we are trying to access is a public path, go on to the route
    if request.url.path in public_paths:
        return await call_next(request)

    # otherwise, get the token from the header and validate it
    token = request.headers.get("authorization")
    response = check_token(token)
    
    # if the token validation is not successful, return the response from check_token which contains the error
    if response.status_code != status.HTTP_200_OK: 
        return response

    # if the token validation is successful (200 OK), then go on to the route and pass the decoded token (response)
    request.state.user = response
    return await call_next(request)
