import uuid


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_uuid(length):
    uid = uuid.uuid4().hex
    return uid[:length].upper()
