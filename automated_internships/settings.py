import datetime

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    authjwt_secret_key: str
    expiration_token_time: datetime.timedelta = datetime.timedelta(days=5)


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
