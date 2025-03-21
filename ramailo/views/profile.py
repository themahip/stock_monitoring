
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ramailo.builders.response_builder import ResponseBuilder
from ramailo.services.profile_service import ProfileService
from ramailo.helpers.user_helper import get_current_user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def streak(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        status, message, details = ProfileService().get_streak_details(user)
        return response_builder.result_object(details).success().ok_200().message(message).get_response()
    except AttributeError as e:
        return Response({"error": "Invalid data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
