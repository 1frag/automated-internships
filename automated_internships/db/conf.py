import os


TORTOISE_ORM = {
    "connections": {"default": os.environ["DATABASE_URL"]},
    "apps": {
        "app": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
