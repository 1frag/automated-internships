from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

from automated_internships.db.models import Users


RegistrationInput = pydantic_model_creator(Users, include=("login", "password"))
LoginInput = pydantic_model_creator(Users, include=("login", "password"))


class LoginOutput(BaseModel):
    token: str
