import asyncio
import logging

from fastapi import Security, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

import utils
from . import forms
from core.settings import settings
from db import models
from controllers.email_ctl import EmailManager

router = InferringRouter()
api_key_header = APIKeyHeader(name="admin", auto_error=False)


@cbv(router)
class RegistrationHandler:
    @router.post("/registration", responses={
        201: {"class": JSONResponse},
        400: {"class": JSONResponse},
        403: {"class": JSONResponse},
    })
    async def registration(
            self,
            in_forms: list[forms.RegistrationInput],
            token: str = Security(api_key_header),
    ):
        """Регистрация нового пользователя"""

        if token != settings.admin_api_key:
            raise HTTPException(status_code=403)

        users = [(pwd := utils.auth.generate_password(), models.User(
            email=form.email,
            first_name=form.first_name,
            last_name=form.last_name,
            password=utils.auth.get_password(pwd)
        )) for form in in_forms]

        async with in_transaction() as conn:

            try:
                created = await asyncio.gather(*(
                    user.save(using_db=conn) for _, user in users
                ))
            except IntegrityError as e:
                return JSONResponse(status_code=400, content={"reason": repr(e), "stage": "db"})

            em = EmailManager()
            try:
                await asyncio.gather(*(
                    em.send_email_with_new_password(user, pwd) for pwd, user in users
                ))
            except Exception as e:
                logging.exception("stage: email; " + repr(e))
                await conn.rollback()
                return JSONResponse(status_code=400, content={"reason": repr(e), "stage": "email"})

        return JSONResponse(status_code=201, content={"created": len(created)})
