from django.conf import settings
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ramailo.helpers.db_helper import get_uuid
from ramailo.builders.response_builder import ResponseBuilder
from ramailo.serializers.kyc_serializer import KycSerializer
from ramailo.services.kyc_service import KycService
from ramailo.helpers.user_helper import get_current_user
from shared.helpers.logging_helper import logger


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='post:set_email', rate=settings.EMAIL_REQUEST_RATE_LIMIT, block=False)
def set_email(request):
    response_builder = ResponseBuilder()
    try:
        if getattr(request, 'limited', False):
            return response_builder.fail().bad_request_400().message("Limit Exceeded! Try again after some time.").get_response()

        token = get_uuid(24)
        user = get_current_user(request)

        serializer = KycSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(f"set_email: serializer exception: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message("Invalid data").get_response()

        status, message, details = KycService(token).save_email(user, **serializer.data)
        if not status == 1:
            logger.info(f"Email sent failed - {status} {message}")
            return response_builder.fail().bad_request_400().message(message).get_response()

        return response_builder.success().ok_200().message(message).get_response()
    except Exception as e:
        logger.exception(f"set_email:: exception:: {e}")
        return response_builder.result_object({"message": "Unable to set email"}).fail().internal_error_500().message("Internal Error").get_response()


@api_view(['GET'])
def verify_email(request, token):
    kyc_service = KycService(token)
    status, message, details = kyc_service.verify_email()
    if not status == 1:
        logger.info(f"Email verify failed - {status} {message}")
        response = render(request, "404.html", context={"message": message})
        response.status_code = 404
        return response

    return render(request, "email_verified_template.html", context={"link": settings.APP_URL})
