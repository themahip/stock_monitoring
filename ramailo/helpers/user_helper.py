import os

from django.shortcuts import get_object_or_404

from ramailo.models.user import User

TEST_USER_MOBILE = os.environ.get("TEST_USER_MOBILE", "7762933208")


def get_current_user(request):
    return get_object_or_404(User, id=request.user.id)
