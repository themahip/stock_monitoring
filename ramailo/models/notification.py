from django.db import models

from ramailo.models.base import BaseModel
from ramailo.models.user import User


class FCMDevice(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fcm_device')
    fcm_token = models.TextField(max_length=350)

    def __str__(self):
        return str(self.user)

    @classmethod
    def create_fcm_device(cls, user, token):
        return cls.objects.update_or_create(user_id=user.id, defaults={"fcm_token": token})
