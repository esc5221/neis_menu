from django.contrib.auth import get_user_model, authenticate

from ninja import Router
from ninja_jwt.tokens import AccessToken

from users.schemas import UserDTO, UserTokenDTO, UserSignupParams, UserLoginParams

router = Router(tags=["users"])

User = get_user_model()


@router.post("/signup/", response=UserTokenDTO, auth=None)
def users_signup(request, data: UserSignupParams = (...)):
    user = User.objects.create_user(**data.dict())
    token = AccessToken.for_user(user)
    return {"user": user, "token": str(token)}


@router.post("/login/", response=UserTokenDTO, auth=None)
def users_login(request, data: UserLoginParams = (...)):
    user = authenticate(**data.dict())
    token = AccessToken.for_user(user)
    return {"user": user, "token": str(token)}


@router.get("/me/", response=UserDTO)
def users_me(request):
    return request.user
