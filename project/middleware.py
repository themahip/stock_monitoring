import threading
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from ramailo.models.user import User

thread_local = threading.local()

class UserLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization", "")
        if token.startswith("Bearer "):
            try:
                jwt_token = token.replace("Bearer ", "")
                token = AccessToken(jwt_token)
                user_id = token.payload.get("id")
                user = get_object_or_404(User, id=user_id)
                user_idx = str(user.idx)
            except Exception as e:
                user_idx = None
        else:
            user_idx = None
        thread_local.user_idx = user_idx
        response = self.get_response(request)
        return response