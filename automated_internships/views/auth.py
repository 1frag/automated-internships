from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import IntegrityError

from .. import forms, utils
from ..settings import settings
from ..db import models

router = InferringRouter()


@cbv(router)
class LoginHandler:
    @router.post("/login", responses={
        401: {"class": JSONResponse},
    })
    async def login(
            self,
            form: forms.LoginInput,
            authorize: AuthJWT = Depends()
    ) -> forms.LoginOutput:
        """Получение JWT токена для выполнения последующих операций"""

        user = await models.Users.get_or_none(login=form.login)
        if (user is None) or (not utils.auth.check_password(form.password, user.password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = authorize.create_access_token(
            subject=user.login, expires_time=settings.expiration_token_time
        )
        return forms.LoginOutput(token=access_token)


@cbv(router)
class RegistrationHandler:
    @router.post("/registration", responses={
        201: {"class": JSONResponse},
        400: {"class": JSONResponse},
    })
    async def registration(
            self, form: forms.RegistrationInput
    ):
        """Регистрация нового пользователя"""

        try:
            await models.Users.create(
                login=form.login,
                password=utils.auth.get_password(form.password)
            )
        except IntegrityError as e:
            if 'unique constraint "users_login_key"' in e.args[0].args[0]:
                return JSONResponse(status_code=400, content={"reason": "Login already exists"})

            return JSONResponse(status_code=500, content={"reason": repr(e)})

        return JSONResponse(status_code=201, content={"status": "Success"})


@cbv(router)
class AuthCheck:
    @router.get("/check")
    async def check(
            self,
            authorize: AuthJWT = Depends(),
            token: str = Depends(utils.deps.auth)
    ):
        """Ручка проверки авторизации"""

        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        return JSONResponse(status_code=200, content={"login": current_user})
