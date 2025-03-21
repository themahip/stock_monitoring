from shared.helpers.logging_helper import logger
from ramailo.models.user import User
from ramailo.services.otp_service import OtpService
from ramailo.services.auth_service import generate_token


class OnboardingService():

    def __init__(self):
        pass

    def onboard_user(self, mobile):
        user, is_created = User.get_or_create_user(mobile)
        otp_status, message = OtpService().generate_otp(user.mobile, user.device_signature)
        if not otp_status:
            logger.info(
                f"OnboardingService onboard_user:: Failed to send OTP to {user}:: {message}")
            return user, False, {'message': "Failed to send OTP"}

        return user, True, {"message": "User is onboarded successfully", "code": "0000"}

    def validate_user(self, mobile, otp, token=""):
        user = User.objects.get(mobile=mobile)
        if not user:
            logger.info(
                f"OnboardingService validate_user:: No user record found for this mobile {mobile}")
            return None, False, {"message": "No user record found."}

        # Validate OTP
        validated = OtpService().validate_otp(mobile, otp)
        if not validated:
            return user, False, {'message': "Invalid OTP"}

        # Generate a token for the user
        token = generate_token(user)

        # Prepare the response
        result = {
            'message': "OTP Verified",
            'token': token,
        }

        return user, True, result

    @staticmethod
    def logout(user, token):
        try:
            pass
            # Logout Logic
        except Exception as e:
            logger.info(f"OnboardingService logout:: Unable to logout {user} {e}")
            return False, "Unable to logout", {}
        return True, "Logout success", {}
