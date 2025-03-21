from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


def validate_file_size(file: UploadedFile) -> None:
    MEGABYTE_LIMIT = 5
    filesize = file.size

    if filesize > MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError(f"Max allowed file size is {MEGABYTE_LIMIT}MB")
