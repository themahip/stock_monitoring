from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from user.serializers.user_serializer import UserRegisterSerializer, UserLoginSerializer
from ramailo.builders.response_builder import ResponseBuilder
from shared.helpers.logging_helper import logger
from user.services.auth_services import AuthService


class UserRegisterView(generics.CreateAPIView):
    """view for user registration"""
    serializer_class= UserRegisterSerializer
    def post(self,request, *args, **kwargs):
        serializer= self.get_serializer(data= request.data)
        response_builder= ResponseBuilder()

        if not serializer.is_valid():
            logger.info(f"registration post:: serializer error: {serializer.errors}")
            error_message=", ".join(["{}: {}".format(key, ", ".join(value))
                                     for key, value in serializer.errors.items()]) 
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()
        username= serializer.validated_data.get('username')
        email= serializer.validated_data.get('email')
        name= serializer.validated_data.get('name')
        password= serializer.validated_data.get('password')
    
        try:
            user, regsitered, details= AuthService().register_user(username=username, email=email, name= name, password=password)
            if not regsitered:
                return response_builder.result_object(details).fail().bad_request_400().message("Registration failed").get_response()
            return response_builder.result_object(details).success().ok_200().message("User Sucessfully Registered").get_response()
        except AttributeError as e:
            logger.info(f"user registration failed:: {e}")
            return response_builder.result_object({'message': "Unable to register user"}).fail().internal_error_500().message("Internal Error").get_response()

class UserLoginView(TokenObtainPairView):
    """View for user login"""
    serializer_class = UserLoginSerializer
    authentication_classes = []  # No authentication required for login
    permission_classes = []     # No permissions required for login

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: "User logged in successfully",
            400: "Invalid credentials",
            500: "Internal server error"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response_builder = ResponseBuilder()

        if not serializer.is_valid():
            logger.info(f"Login post:: serializer errors: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value)) 
                                     for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user, authenticated, details = AuthService.login_user(email=email, password=password)
            if not authenticated:
                logger.info(f"Login failed for {email}: {details.get('message')}")
                return response_builder.result_object(details).fail().bad_request_400().message("Invalid credentials").get_response()
            
            logger.info(f"User {email} logged in successfully")
            return response_builder.result_object(details).success().ok_200().message("User logged in successfully").get_response()
        except Exception as e:
            logger.exception(f"Login post:: exception:: {e}")
            return response_builder.result_object({'message': "Unable to login user"}).fail().internal_error_500().message("Internal Error").get_response()