from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.transactions import in_transaction

import utils
from . import forms
from core.settings import settings
from db import models
from controllers.email_ctl import EmailManager

router = InferringRouter()


@cbv(router)
class LoginHandler:
    @router.post("/login", responses={
        401: {"class": JSONResponse},
    })
    async def login(
            self,
            form: forms.LoginInput,
            authorize: AuthJWT = Depends(),
    ) -> forms.LoginOutput:
        """Получение JWT токена для выполнения последующих операций"""

        user = await models.User.get_or_none(email=form.email)
        if (user is None) or (not utils.auth.check_password(form.password, user.password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = authorize.create_access_token(
            subject=user.email, expires_time=settings.expiration_token_time
        )
        return forms.LoginOutput(token=access_token)


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
        return JSONResponse(status_code=200, content={"email": current_user})


@cbv(router)
class ChangePassword:
    @router.post("/change_password/get_secret_code")
    async def get_secret_code(
            self,
            email: str,
    ):
        """Ручка, чтобы скинули код на заполнение нового пароля в email"""

        user = await models.User.get_or_none(email=email)
        if user is None:
            raise HTTPException(status_code=404)

        action = models.ChangePassword(
            user=user,
            value=utils.auth.generate_password(),
            active=True,
        )

        async with in_transaction() as conn:
            await action.save(using_db=conn)
            await EmailManager().send_link_to_change_password(user, action)
        raise HTTPException(status_code=204)

    @router.post("/change_password/by_secret_code")
    async def by_secret_code(
            self,
            secret_value: str,
            new_password: str,
    ):
        """Ручка, чтобы поменять пароль с помощью кода из get_secret_code"""

        action = await models.ChangePassword.get_or_none(value=secret_value).prefetch_related("user")
        if action is None:
            raise HTTPException(status_code=403)

        user: models.User = action.user
        user.password = utils.auth.get_password(new_password)
        await user.save()
        raise HTTPException(status_code=204)

    @router.post("/change_password/by_auth")
    async def by_auth(
            self,
            new_password: str,
            authorize: AuthJWT = Depends(),
            token: str = Depends(utils.deps.auth),
    ):
        """Ручка, чтобы поменять пароль с помощью JWT токена"""

        authorize.jwt_required()
        email = authorize.get_jwt_subject()
        user = await models.User.get_or_none(email=email)

        if user is None:
            raise HTTPException(status_code=403)

        user.password = utils.auth.get_password(new_password)
        await user.save()
        raise HTTPException(status_code=204)
