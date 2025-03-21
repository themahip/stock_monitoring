import random

from django.conf import settings

from ramailo.accessors.sms_accessor import SMSAccessor
from shared.helpers.logging_helper import logger

from .cache_service import RedisService

OTP_EXPIRY = 120
USE_REDIS = True
DEFAULT_OTP = "123456"
TEST_OTP = "679008"


class OtpService():

    def __init__(self):
        self.client = SMSAccessor()
        self.success_message = "OTP has been generated successfully"
        self.failure_message = "Failed to send otp"
        self.cache = RedisService.get_instance()

    def generate_otp(self, mobile, signature):
        # TODO - rate limiter [5 requests per 3 min for one IP or mobile]
        if settings.DEBUG:
            return DEFAULT_OTP, self.success_message

        if mobile in settings.TESTERS:
            return TEST_OTP, self.success_message

        otp = self.client.send(mobile, signature)
        if not otp:
            return False, self.failure_message
        if USE_REDIS:
            self.cache.set("otp_" + mobile, otp, OTP_EXPIRY)
        return True, self.success_message

    def validate_otp(self, mobile, otp):
        if settings.DEBUG:
            return otp == DEFAULT_OTP

        if mobile in settings.TESTERS:
            return otp == TEST_OTP

        if USE_REDIS:
            logger.info(f"Verifying otp from redis {mobile}")
            otp_in_redis = self.cache.get("otp_" + mobile)
            if otp_in_redis == otp:
                logger.info(f"OTP verified from redis {mobile}")
                self.cache.delete("otp_" + mobile)
                return True
            return False

        logger.info(f"Verifying otp from msg91 {mobile}")
        return self.client.verify(mobile, otp)

    def generate_email_otp(self, user):
        key = str(user.idx)
        otp_in_redis = self.cache.get(key)
        if otp_in_redis:
            return True, None
        otp = random.randint(100000, 999999)
        self.cache.set(key=key, value=otp, timeout=settings.EMAIL_OTP_EXPIRY)
        return False, otp

    def validate_email_otp(self, user, otp):
        key = str(user.idx)
        otp_in_redis = self.cache.get(key)
        if otp_in_redis == str(otp):
            self.cache.delete(key)
            return True
        return False
