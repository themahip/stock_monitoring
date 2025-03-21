from rest_framework.decorators import api_view

from ramailo.builders.response_builder import ResponseBuilder


@api_view(['GET'])
def health(request):
    response_builder = ResponseBuilder()
    return response_builder.result_object({}).success().ok_200().message("Health check").get_response()
