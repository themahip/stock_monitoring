from celery.app import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from pyfcm import FCMNotification

from ramailo.accessors.sms_accessor import SMSAccessor
from ramailo.models.notification import FCMDevice
from ramailo.services.email_service import send_email
from shared.helpers.logging_helper import logger


class NotificationService():

    @staticmethod
    def create_update_fcm_device(user, token):
        FCMDevice.create_fcm_device(user, token)
        return

    @staticmethod
    @shared_task(name='send_notification')
    def send_push_notification(title, body, user_id=None, image_url=None):
        key = settings.FCM_API_KEY
        push_service = FCMNotification(api_key=key)
        extra = {'image': image_url}

        if user_id:
            try:
                token = FCMDevice.objects.get(user_id=user_id).fcm_token
                logger.info(
                    f"send_push_notification to user: {user_id} token: {token} title: {title} body: {body}")
                push_service.notify_single_device(
                    registration_id=token, message_title=title, message_body=body, extra_notification_kwargs=extra)
            except FCMDevice.DoesNotExist:
                logger.info(f"send_push_notification fcm_token doesn't exist for user: {user_id}")
                pass
            return

        tokens = list(FCMDevice.objects.all().values_list("fcm_token", flat=True))
        logger.info(f"send_push_notification multiple title: {title} body: {body}")
        push_service.notify_multiple_devices(
            registration_ids=tokens, message_title=title, message_body=body, extra_notification_kwargs=extra)
        return

    @staticmethod
    def send_sms_notification(mobile, msg, msg2):
        logger.info(f"Sending sms notification to mobile: {mobile} msg: {msg} msg2: {msg2}")
        return SMSAccessor().send_sms(mobile, msg, msg2)

    @staticmethod
    def send_email_notification(subject, body, email=None, attachment=None):
        if email:
            logger.info(f"Sending email notification to email: {email} body: {body}")
            send_email.delay(subject, body, [email], attachment)

    @staticmethod
    def send_email_notification_template(subject, template, email=None, attachment=None, details={}):
        if email:
            logger.info(
                f"Sending email notification template to email: {email} template: {template} details: {details}")
            body = render_to_string(template, details)
            send_email.delay(subject, body, [email], attachment)
