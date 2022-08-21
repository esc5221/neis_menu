from typing import Optional

from django.contrib.auth import get_user_model

from ninja import Schema, ModelSchema
User = get_user_model()


class UserDTO(ModelSchema):

    class Config:
        model = User
        model_fields = ["id", "username", "email"]


class UserTokenDTO(Schema):
    user: UserDTO
    token: str


class UserSignupParams(Schema):
    username: str
    password: str
    email: Optional[str] = None
    first_name: str
    last_name: str


class UserLoginParams(Schema):
    username: str
    password: str
