from celery.app import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from shared.helpers.logging_helper import logger


@shared_task(name='send_email')
def send_email(subject: str, body: str, receiver: list, attachment=None):
    logger.info(f"Sending {subject} Mail to: {receiver}")
    sender = '{} <{}>'.format(settings.COMPANY_NAME, settings.AWS_SES_EMAIL)

    email = EmailMessage(subject, body, sender, receiver)
    if attachment:
        email.attach(**attachment)
    email.content_subtype = 'html'
    email.fail_silently = True
    email.send()


def send_verification_email(user, otp):
    receiver = [user.email]
    template = "email_verification_template.html"

    subject = "Request For Email Verification"
    body = render_to_string(template, {
        'name': user.get_name(),
        'otp': otp,
        'company_name': settings.COMPANY_NAME,
        'link': settings.APP_URL
    })
    send_email.delay(subject, body, receiver)


def send_link_based_verification_email(user, link):
    receiver = [user.email]
    template = "email_verification_link_template.html"

    subject = "Request For Email Verification"
    body = render_to_string(template, {
        'name': user.get_name(),
        'link': link,
        'company_name': settings.COMPANY_NAME,
        'expiry': int(settings.EMAIL_LINK_EXPIRY / 60)
    })
    send_email.delay(subject, body, receiver)
