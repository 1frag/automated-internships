import os


TORTOISE_ORM = {
    "connections": {"default": os.environ["DATABASE_URL"]},
    "apps": {
        "app": {
            "models": ["automated_internships.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
