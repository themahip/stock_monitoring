from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ramailo.builders.response_builder import ResponseBuilder
from ramailo.serializers.onboarding_serializer import FCMSerializer
from ramailo.services.notification_service import NotificationService
from ramailo.helpers.user_helper import get_current_user
from shared.helpers.logging_helper import logger


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_fcm_device(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        serializer = FCMSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(f"set_email: serializer exception: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()
        NotificationService.create_update_fcm_device(
            user, token=serializer.validated_data["fcm_token"])
        return response_builder.success().ok_200().message("FCM Device Registered").get_response()
    except AttributeError as e:
        return response_builder.result_object({"message": "Unable to set fcm device"}).fail().internal_error_500().message("Internal Error").get_response()
