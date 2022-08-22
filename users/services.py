from typing import Tuple

from django.contrib.auth import get_user_model, authenticate

from ninja_jwt.tokens import AccessToken

from users.schemas import UserDTO, UserTokenDTO, UserSignupParams, UserLoginParams

User = get_user_model()


def UserSignupService(data: UserSignupParams) -> Tuple[User, AccessToken]:
    user = User.objects.create_user(**data.dict())
    token = AccessToken.for_user(user)
    return user, token


def UserLoginService(data: UserSignupParams) -> Tuple[User, AccessToken]:
    user = authenticate(**data.dict())
    token = AccessToken.for_user(user)
    return user, token
