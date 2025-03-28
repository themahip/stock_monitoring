from ramailo.services.auth_service import generate_token
from shared.helpers.logging_helper import logger
from rest_framework_simplejwt.tokens import RefreshToken

from user.models.user import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthService:
    @staticmethod
       
    def register_user(username, name, email, password):
        """handle user registration"""
        user= User()
        if User.objects.filter(email= email).exists():
                logger.info(f"Registration attempt with already existing email: {email}")
                return user, False, {"message":"Email already exist"}
        if User.objects.filter(username=username).exists():
                logger.info(f"attempt to user already used username by: {username} ")
                return user, False,{"Message":"username already exist"}
     
        user.setpassword(password)
        user.create_user(email=email, name=name, username=username)
        result= {
             "message":"user registration done",
        }
        return user, True, result
    
    @staticmethod

    def login_user(email, password):
        """Handle user login with email and password"""
        try:
            user = User.objects.get(email=email)
            if user.authenticate_user(password):
                tokens = generate_token(user=user)
                result = {
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username,
                    **tokens
                }
                logger.info(f"User {email} logged in successfully")
                return user, True, result
            else:
                logger.info(f"Login failed for {email}: Invalid password")
                return None, False, {"message": "Invalid password"}
        except User.DoesNotExist:
            logger.info(f"Login attempt with non-existent email: {email}")
            return None, False, {"message": "User not found"}
        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            return None, False, {"message": str(e)}

            