from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from ramailo.builders.response_builder import ResponseBuilder
from ramailo.helpers.view_helper import get_auth_token
from ramailo.openapi.schema import PROFILE_API
from ramailo.serializers.onboarding_serializer import (
    LoginSerializer,
    OnboardingSerializer,
)
from ramailo.services.onboarding_service import OnboardingService
from ramailo.helpers.user_helper import get_current_user
from shared.helpers.logging_helper import logger


class OtpView(APIView):

    @swagger_auto_schema(**PROFILE_API)
    def post(self, request, *args, **kwargs):
        serializer = OnboardingSerializer(data=request.data)
        response_builder = ResponseBuilder()

        if not serializer.is_valid():
            logger.info(f"otp post:: {user} serializer errors:: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()

        mobile = serializer.validated_data.get('mobile')
        logger.info(f"otp post:: OnboardingSerializer.data = {serializer.validated_data}", )

        try:
            user, status, details = OnboardingService().onboard_user(mobile)

            if not status:
                logger.info(f"otp post:: Unable to onboard user {user} :: {details}")
                return response_builder.result_object(details).fail().bad_request_400().message("Not authorized to login to new device").get_response()

            return response_builder.result_object(details).success().ok_200().message("OTP Sent").get_response()
        except AttributeError as e:
            logger.exception(f"otp post:: exception:: {e}")
            return response_builder.result_object({'message': "Unable to onboard user"}).fail().internal_error_500().message("Internal Error").get_response()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response_builder = ResponseBuilder()

        if not serializer.is_valid():
            logger.info(f"otp post:: {user} serializer errors:: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()

        mobile = serializer.validated_data.get('mobile')
        otp = serializer.validated_data.get('otp')

        try:
            token = get_auth_token(request)
            user, validated, details = OnboardingService().validate_user(mobile, otp, token=token)
            if not validated:
                return response_builder.result_object(details).fail().bad_request_400().message("Invalid OTP").get_response()
            return response_builder.result_object(details).success().ok_200().message("OTP Verified").get_response()
        except AttributeError as e:
            logger.exception(f"login post:: exception:: {e}")


@api_view(['POST'])
def logout(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        token = get_auth_token(request)
        status, message, details = OnboardingService().logout(user, token)
        if not status:
            logger.info(f"otp post:: Unable to logout user {user} :: {message} {details}")
            return response_builder.result_object(details).fail().internal_error_500().message(message).get_response()
        return response_builder.result_object(details).success().ok_200().message(message).get_response()
    except AttributeError as e:
        logger.exception(f"logout:: exception:: {e}")
        return response_builder.result_object({"message": "Unable to logout"}).fail().internal_error_500().message("Internal Error").get_response()
