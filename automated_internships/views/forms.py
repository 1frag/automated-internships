from pydantic import BaseModel


class RegistrationInput(BaseModel):
    email: str
    first_name: str
    last_name: str


class LoginInput(BaseModel):
    email: str
    password: str


class LoginOutput(BaseModel):
    token: str
