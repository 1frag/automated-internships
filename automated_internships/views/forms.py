from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

from db.models import User


RegistrationInput = pydantic_model_creator(User, include=("login", "password"))
LoginInput = pydantic_model_creator(User, include=("login", "password"))


class LoginOutput(BaseModel):
    token: str
