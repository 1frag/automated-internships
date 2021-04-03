import asyncio
from tortoise import Tortoise

from db import conf, models

init = Tortoise.init(config=conf.TORTOISE_ORM)
