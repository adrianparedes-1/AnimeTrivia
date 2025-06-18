from fastapi import FastAPI, APIRouter
from modules.user.routers import user_router
app = FastAPI()
router = APIRouter()


app.include_router(
    user_router.router
)