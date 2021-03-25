from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=63, unique=True)
    password = fields.CharField(max_length=127)
