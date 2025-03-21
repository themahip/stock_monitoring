from drf_yasg import openapi

SAMPLE_API = {
    "operation_description": "Returns response in this format",
    "responses": {
        200: openapi.Response(
            description='Success',
            examples={
                "application/json": {
                    "data": {
                        "name": "Anup Singh"
                    }
                }
            }
        ),
        400: openapi.Response(
            description='Success',
            examples={
                "application/json": {
                    "data": {
                        "message": "Bad Request"
                    }
                }
            }
        ),
    }
}

PROFILE_API = {
    "operation_description": "This returns user profile response",
    "responses": {
        200: openapi.Response(
            description='Success',
            examples={
                "application/json": {
                    "name": "Anup Singh"
                }
            }
        )
    }
}
