from fastapi import FastAPI, APIRouter, Depends
from modules.user.routers import user_router
from modules.menu.routers import menu_router
from db.session_manager import get_db
from sqlalchemy.orm import Session
from modules.user.models.user_models import UserORM
app = FastAPI()
router = APIRouter()


app.include_router(user_router.router)
app.include_router(menu_router.router)


@app.get("/test")
def test(db: Session = Depends(get_db)):
    return db.query(UserORM).all()