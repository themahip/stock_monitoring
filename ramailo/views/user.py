from django_ratelimit.decorators import ratelimit
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken

from ramailo.builders.response_builder import ResponseBuilder
from ramailo.middlewares.device_authentication import IsDeviceAuthenticated
from ramailo.openapi.schema import PROFILE_API
from ramailo.serializers.user_serializer import (
    KycSerializer,
    ProfileUpdateSerializer,
)
from ramailo.services.user_service import UserService
from ramailo.helpers.user_helper import get_current_user
from shared.helpers.logging_helper import logger


class ProfileView(APIView):
    permission_classes = [IsDeviceAuthenticated]

    @swagger_auto_schema(**PROFILE_API)
    def get(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        try:
            user = get_current_user(request)
            return response_builder.result_object(user.profile()).success().ok_200().get_response()
        except Exception as e:
            logger.exception(f"ProfileView get :: exception:: {e}")
            return response_builder.result_object({'message': "Unable to get profile"}).fail().internal_error_500().message("Internal Error").get_response()

    def put(self, request, *args, **kwargs):
        try:
            user = get_current_user(request)
            serializer = ProfileUpdateSerializer(user, data=request.data)
            response_builder = ResponseBuilder()

            if not serializer.is_valid():
                logger.info(f"profile put:: {user} serializer errors:: {serializer.errors}")
                error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                          for key, value in serializer.errors.items()])
                return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()

            serializer.save()
            return response_builder.result_object(serializer.data).success().ok_200().message("Profile updated").get_response()
        except InvalidToken:
            return response_builder.result_object({'detail': 'Invalid token! Please provide a valid token.'}).fail().bad_request_400().get_response()
        except Exception as e:
            logger.exception(f"ProfileView put:: exception:: {e}")
            return response_builder.result_object({'message': "Unable to update profile"}).fail().internal_error_500().message("Internal Error").get_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='post:kyc', rate='3/5m', block=False)
def kyc(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        serializer = KycSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(f"kyc post:: {user} serializer errors:: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()
        status, message, response = UserService.verify_kyc(user, kyc_data=serializer.validated_data)

        logger.info(f"verify_kyc: {status}, {message}, {response}")
        if status != 1:
            return response_builder.result_object(response).fail().bad_request_400().message(message).get_response()
        return response_builder.result_object(serializer.data).success().ok_200().message(message).get_response()
    except AttributeError as e:
        logger.exception(f"kyc post:: exception:: {e}")
        return response_builder.result_object({"message": "Unable to create kyc"}).fail().internal_error_500().message("Internal Error").get_response()
