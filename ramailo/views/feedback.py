from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ramailo.builders.response_builder import ResponseBuilder
from ramailo.serializers.feedback_serializer import (
    FeedbackSerializer,
    RaiseTicketSerializer,
)
from ramailo.helpers.user_helper import get_current_user
from shared.helpers.logging_helper import logger


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feedback(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        request_data = request.data
        request_data["user"] = user.id
        serializer = FeedbackSerializer(data=request_data)
        if not serializer.is_valid():
            logger.info(f"feedback: serializer exception: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()
        serializer.save()
        return response_builder.result_object({"message": "Feedback Received Successfully"}).success().ok_200().message("Feedback Received").get_response()
    except AttributeError as e:
        logger.exception(f"feedback:: exception:: {e}")
        return response_builder.result_object({"message": "Unable to create feedback"}).fail().internal_error_500().message("Internal Error").get_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def raise_ticket(request):
    response_builder = ResponseBuilder()
    try:
        user = get_current_user(request)
        request_data = request.data
        request_data["user"] = user.id
        serializer = RaiseTicketSerializer(data=request_data)
        if not serializer.is_valid():
            logger.info(f"feedback: serializer exception: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value))
                                      for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()
        return response_builder.result_object({"message": "Ticket Received Successfully"}).success().ok_200().message("Ticket Received").get_response()
    except AttributeError as e:
        logger.exception(f"raise_ticket:: exception:: {e}")
        return response_builder.result_object({"message": "Unable to raise ticket"}).fail().internal_error_500().message("Internal Error").get_response()
