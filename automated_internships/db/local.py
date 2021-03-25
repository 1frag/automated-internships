import asyncio
from tortoise import Tortoise

from . import conf

asyncio.run(Tortoise.init(config=conf.TORTOISE_ORM))
