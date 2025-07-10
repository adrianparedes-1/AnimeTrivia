from starlette_admin.contrib.sqla import Admin, ModelView
from db.session_manager import engine
from modules.user.models.user_model import UserORM
from modules.menu.models.profile_model import ProfileORM

# initialize starlette admin
admin = Admin(engine, title="AnimeTrivia Admin")
admin.add_view(ModelView(UserORM))
admin.add_view(ModelView(ProfileORM))