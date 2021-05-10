from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    """
    Reference https://github.com/IndominusByte/fastapi-jwt-auth/blob/master/examples/generate_doc.py
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Automated Internships",
        version="0.1.0",
        description="Documentation for Automated Internships Service",
        routes=app.routes,
    )

    headers = {
        "name": "Authorization",
        "in": "header",
        "required": False,
        "description": "Ожидается JWT token в Authorization или Cookie",
        "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwaXNrdW5vdi5hbGVzaGFAZ2",
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    for route in (
            route for route in app.routes
            if isinstance(route, APIRoute) and route.operation_id == "authorize"
    ):
        method = list(route.methods)[0].lower()
        try:
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            openapi_schema["paths"][route.path][method].update({"parameters": [headers]})

    app.openapi_schema = openapi_schema
    return app.openapi_schema
