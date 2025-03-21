from django.conf import settings
from django.utils import timezone

from ramailo.helpers.db_helper import get_or_none
from ramailo.models.kyc import EmailVerification
from ramailo.models.user import Kyc
from ramailo.services.email_service import send_link_based_verification_email
from shared.helpers.logging_helper import logger


class KycService():

    def __init__(self, token):
        self.verification = None
        try:
            self.verification = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist as e:
            logger.info(f"{token} does not exists in database, creating one for this user")
            self.verification = EmailVerification(token=token)

    @staticmethod
    def get_kyc_details(user):
        return get_or_none(Kyc, user_id=user.id)

    @staticmethod
    def create_kyc_details(user, name, dob, file):
        return Kyc.create_kyc(user, name, dob, file)

    @staticmethod
    def filter_kyc(filters):
        return Kyc.filter_kyc(filters)

    @staticmethod
    def verify_kyc(user, kyc_data):
        name = user.name
        dob = kyc_data["dob"]
        file = kyc_data["file"]

        kyc = KycService.get_kyc_details(user)
        if kyc:
            if kyc.status == "Pending":
                return 0, "You already have one pending KYC request", {}

            if kyc.status == "Approved":
                return 0, "Your KYC was already approved", {}

        if not kyc:
            KycService.create_kyc_details(user, name, dob, file)

        kyc.status = "Pending"
        kyc.save()

        return 1, "Your KYC has been submitted and is under processing", {}

    def is_token_expired(self):
        return self.verification.expiration_time < timezone.now()

    def generate_link(self, user):
        verification_link = f'{settings.WEB_URL}kyc/email/validate/{self.verification.token}/'
        self.verification.expiration_time = timezone.now() + timezone.timedelta(seconds=settings.EMAIL_LINK_EXPIRY)
        self.verification.user = user
        self.verification.save()
        return verification_link

    def save_email(self, user, email):

        if user.is_email_verified:
            return 0, f"Verified Email - '{user.email}' Already Exists for user", {}

        # Check if email is already sent to that user
        tmp = EmailVerification.objects.filter(user=user, expiration_time__gt=timezone.now())
        if tmp:
            return 0, f"Email already sent", {}

        user.email = email
        user.save()
        logger.info(f"Email - {email} of user {user.name} updated in database")

        link = self.generate_link(user)
        logger.info(f"Sending linked based verification email to {email}")
        send_link_based_verification_email(user, link)
        logger.info(f"Linked based verification email sent to {email}")

        return 1, "Link sent to Email for Verification", {}

    def verify_email(self):

        if not hasattr(self.verification, 'user'):
            return 0, "Invalid link", {}

        if self.is_token_expired():
            return 0, "Token has expired", {}

        user = self.verification.user
        user.is_email_verified = True
        user.save()
        self.verification.delete()
        return 1, "Successfully verified", {}
