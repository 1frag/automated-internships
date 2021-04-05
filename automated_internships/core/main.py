from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from tortoise.contrib.fastapi import register_tortoise
from fastapi_admin.factory import app as admin_app
from fastapi_admin.site import Site

from views import auth, admin
from db.conf import TORTOISE_ORM
from core.utils import custom_openapi

app = FastAPI(debug=True)

app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(admin.router, prefix="/v1/admin", tags=["admin"])


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# tortoise
register_tortoise(app, config=TORTOISE_ORM)

# admin page
app.mount('/api/admin', admin_app)


@app.on_event('startup')
async def startup():
    await admin_app.init(
        admin_secret="test",
        permission=True,
        site=Site(
            name="Automated internships dashboard",
            login_footer="Automated internships dashboard",
            login_description="Automated internships dashboard",
            locale="en-US",
            locale_switcher=True,
            theme_switcher=True,
        ),
    )

app.openapi = lambda: custom_openapi(app)
