import random
import string

from django.conf import settings
from django.core.validators import (
    FileExtensionValidator,
)
from django.db import models, transaction

from ramailo.helpers.file_helper import validate_file_size
from ramailo.models.base import BaseModel
from ramailo.services.storage_service import StorageService


class User(BaseModel):
    mobile = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=128, blank=True, default="")
    name = models.CharField(max_length=255, blank=True, default="")
    age = models.IntegerField(null=True)
    dob = models.DateField(null=True)
    pin_code = models.CharField(max_length=10, blank=True, default="")

    # kyc
    is_email_verified = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)

    # investments
    last_invested_on = models.DateTimeField(null=True)

    # device
    device_signature = models.CharField(max_length=128, blank=True, default="")

    # referral
    referral_id = models.CharField(max_length=10, blank=True, default="")
    referrer_id = models.CharField(max_length=128, blank=True, default="")
    total_rewards = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # waitlist
    is_approved = models.BooleanField(default=False)
    position = models.IntegerField(default=0)

    # others
    validated_on = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name} - {self.mobile}'

    @property
    def is_new_user(self):
        return not self.last_invested_on

    @property
    def is_validated(self):
        return bool(self.validated_on)

    @property
    def image(self):
        try:
            profile_image = ProfileImage.objects.filter(user=self).latest("created_at")
            return profile_image.image_url
        except ProfileImage.DoesNotExist:
            return settings.DUMMY_USER_IMAGE

    def profile(self):
        return {}

    @classmethod
    def get_or_create_user(cls, mobile):
        user, created = cls.objects.get_or_create(mobile=mobile)
        if created:
            user.position = cls.get_last_position()
            user.save()
        return user, created

    def generate_signed_url(self):
        object_key = self.IMAGE_STORAGE_PATH + str(self.image)
        s3_client = StorageService.get_instance()
        return s3_client.generate_presigned_url(object_key)


class ProfileImage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    IMAGE_STORAGE_PATH = 'users/images/'
    image = models.FileField(null=True, upload_to=IMAGE_STORAGE_PATH, validators=[
        validate_file_size, FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png", "pdf"])])

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return settings.DUMMY_USER_IMAGE


class Kyc(BaseModel):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_kyc')
    name = models.CharField(max_length=100)
    dob = models.DateField()
    file = models.FileField(upload_to='kyc/files/', validators=[
                            validate_file_size, FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png", "pdf"])])

    KYC_STATUS_CHOICES = (
        ('Initial',) * 2,
        ('Pending',) * 2,
        ('Approved',) * 2,
        ('Rejected',) * 2,
    )
    status = models.CharField(max_length=10, choices=KYC_STATUS_CHOICES, default="Initial")

    @classmethod
    def filter_kyc(cls, filters):
        return cls.objects.filter(**filters)

    @classmethod
    def create_kyc(cls, user, name, dob, file):
        return cls.objects.create(user_id=user.id, name=name, dob=dob, file=file)
