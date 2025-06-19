from modules.user.dtos.user_create_dto import UserCreateDTO
from modules.user.models.user_models import UserORM
from db.session_manager import get_db

def create(user: UserCreateDTO) -> None:
    db_gen = get_db()  # this is a generator
    db = next(db_gen)  # this gets the actual session instance
    
    query = db.query(UserORM).filter(
        UserORM.email == user.email,
        UserORM.username == user.id 
    ).first()

    if not query:
        user_orm = UserORM(
            username=user.id,  
            email=user.email,
            display_name=user.display_name
        )
        db.add(user_orm)
        db.commit()