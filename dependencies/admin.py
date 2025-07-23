from starlette_admin.contrib.sqla import Admin, ModelView
from db.session_manager import engine
from modules.user.models.user_model import User
from modules.menu.models.profile_model import Profile
from modules.anime.models import (
    anime_orm_model,
    ending_orm_model,
    genre_orm_model,
    image_orm_model,
    opening_orm_model,
    studio_orm_model,
    theme_orm_model,
    title_orm_model,
    topical_theme_orm_model,
    trailer_orm_model
)


# initialize starlette admin
admin = Admin(engine, title="AnimeTrivia Admin")
admin.add_view(ModelView(User))
admin.add_view(ModelView(Profile))
admin.add_view(ModelView(anime_orm_model.Anime))
admin.add_view(ModelView(ending_orm_model.Ending))
admin.add_view(ModelView(opening_orm_model.Opening))
admin.add_view(ModelView(theme_orm_model.Theme))
admin.add_view(ModelView(image_orm_model.Image))
admin.add_view(ModelView(studio_orm_model.Studio))
admin.add_view(ModelView(title_orm_model.Title))
admin.add_view(ModelView(trailer_orm_model.Trailer))
admin.add_view(ModelView(genre_orm_model.Genre))
admin.add_view(ModelView(topical_theme_orm_model.TopicalTheme))