import os


TORTOISE_ORM = {
    "connections": {"default": os.environ["DATABASE_URL"]},
    "apps": {
        "models": {
            "models": ["automated_internships.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
