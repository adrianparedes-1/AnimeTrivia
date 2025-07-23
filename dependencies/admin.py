from starlette_admin.contrib.sqla import Admin, ModelView
from db.session_manager import engine
from modules.user.models.user_model import User
from modules.menu.models.profile_model import Profile
from modules.anime.models import (
    anime_orm_model,
    endings_orm_model,
    openings_orm_model,
    themes_orm_model,
    images_orm_model,
    studios_orm_model,
    titles_orm_model,
    trailer_orm_model,
    genres_orm_model
)


# initialize starlette admin
admin = Admin(engine, title="AnimeTrivia Admin")
admin.add_view(ModelView(User))
admin.add_view(ModelView(Profile))
admin.add_view(ModelView(anime_orm_model.Anime))
admin.add_view(ModelView(endings_orm_model.Endings))
admin.add_view(ModelView(openings_orm_model.Openings))
admin.add_view(ModelView(themes_orm_model.Themes))
admin.add_view(ModelView(images_orm_model.Images))
admin.add_view(ModelView(studios_orm_model.Studios))
admin.add_view(ModelView(titles_orm_model.Titles))
admin.add_view(ModelView(trailer_orm_model.Trailer))
admin.add_view(ModelView(genres_orm_model.Genres))