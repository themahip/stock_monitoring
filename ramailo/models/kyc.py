from django.db import models
from django.utils import timezone

from ramailo.models.base import BaseModel
from ramailo.models.user import User


class EmailVerification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiration_time = models.DateTimeField()
    is_email_sent = models.BooleanField(default=False)

    def is_expired(self):
        return self.expiration_time < timezone.now()

    def __str__(self) -> str:
        return self.token
