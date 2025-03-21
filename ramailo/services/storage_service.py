import boto3
from django.conf import settings

from ramailo.helpers.date_helper import get_today


class StorageService:
    __instance = None

    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.expires_in = 3600
        StorageService.__instance = None
        if StorageService.__instance is None:
            self.__client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            StorageService.__instance = self
        else:
            raise Exception("Can't create more than one instances")

    @staticmethod
    def get_instance():
        if StorageService.__instance is None:
            StorageService()
        return StorageService.__instance

    def generate_presigned_url(self, key):
        return self._StorageService__client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key},
            ExpiresIn=self.expires_in
        )

    @staticmethod
    def user_image_upload_path(instance, filename):
        user_id = instance.idx
        date = get_today()
        new_filename = f"user_{user_id}/profile_image_{str(date)}_{filename}"
        return new_filename
