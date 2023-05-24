from ..routers.dto import user_schemas
from ..db import user_repo


def login(request: user_schemas.AuthRequest):
    return user_repo.create_user(request)
