from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ramailo.models.base import BaseModel
from ramailo.models.user import User


class Feedback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, related_name='user_feedback')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    TYPE_CHOICES = (
        ("Saving experience",) * 2,
        ("Rewards and Benefits",) * 2,
        ("App design",) * 2,
        ("Others",) * 2,
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        if self.type == dict(self.TYPE_CHOICES)["Others"] and not self.message:
            raise ValidationError({"message": "Message is required for type others!"})

    @classmethod
    def filter_feedback(cls, filters):
        return cls.objects.filter(**filters)
