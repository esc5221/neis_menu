from users.api import router as users_router
from schools.api import router as schools_router
from menus.api import router as menus_router


from typing import List, Optional

from ninja import NinjaAPI

from ninja_jwt.authentication import JWTAuth


from django.db.models import F, Count

from schools.models import School
from menus.models import Menu


api = NinjaAPI(title="neis_menu API v2", version="2.0.0", auth=JWTAuth())

api.add_router("/users/", users_router)
api.add_router("/schools/", schools_router)
api.add_router("/menus/", menus_router)
