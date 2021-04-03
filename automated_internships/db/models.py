from tortoise import fields, models
from fastapi_admin.models import (
    AbstractAdminLog, AbstractPermission, AbstractRole, AbstractUser,
)


class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=63)
    last_name = fields.CharField(max_length=63)
    password = fields.CharField(max_length=127)

    class Meta:
        unique_together = (("first_name", "last_name"),)


class AdminUser(AbstractUser):  # only for dashboard
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass


class AdminLog(AbstractAdminLog):
    pass


class ChangePassword(models.Model):
    user = fields.OneToOneField('models.User', pk=True)
    value = fields.CharField(max_length=20, unique=True)
    active = fields.BooleanField(default=False)
