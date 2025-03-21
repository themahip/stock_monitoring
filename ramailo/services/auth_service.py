from rest_framework_simplejwt.tokens import RefreshToken

from ramailo.serializers.onboarding_serializer import RefreshTokenSerializer


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    serializer = RefreshTokenSerializer(refresh)
    return serializer.data
