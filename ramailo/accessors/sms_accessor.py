import json
import os
import random

import requests
from django.conf import settings

from ramailo.constants import DEFAULT_COUNTRY_CODE
from shared.helpers.logging_helper import logger

OTP_LENGTH = 6

# Msg91 stuffs
COMPANY_NAME = "Ramailo"
TEMPLATE_ID = ""
URL = 'http://control.msg91.com/api/'
BASE_URL = os.environ.get("MSG91_BASE_URL")
AUTH_KEY = os.environ.get("MSG91_AUTH_KEY", "")
SENDER_ID = "RAMAILO"
DLT_TE_ID = ""


class SMSAccessor:

    def generate_otp(self, length=OTP_LENGTH):
        lower_bound = 10 ** (OTP_LENGTH - 1)
        upper_bound = (10 ** OTP_LENGTH) - 1
        otp = random.randint(lower_bound, upper_bound)
        return otp

    def format_mobile(self, mobile):
        if len(mobile) == 10:
            return f"{DEFAULT_COUNTRY_CODE}{mobile}"
        return mobile

    def send(self, mobile, signature):
        otp = self.generate_otp()
        mobile = self.format_mobile(mobile)
        # url = BASE_URL + \
        #     f"/otp?template_id={TEMPLATE_ID}&mobile=91{mobile}&otp={otp}"
        signature = signature or "6q9m%2FSEunEW"
        url = URL + \
            f"sendotp.php?otp=123456&authkey=410046AmuRkCnhzboY65649438P1&message=%3C%23%3E%20{otp}%20is%20your%20OTP%20for%20Login,%20Vaild%20for%202%20minutes.%20Please%20Do%20not%20share%20this%20OTP.%20{signature}&sender={SENDER_ID}&mobile={mobile}&DLT_TE_ID={DLT_TE_ID}"
        payload = {
            "mobile": mobile
        }
        headers = {
            'accept': 'application/json',
            'authkey': AUTH_KEY,
            'content-type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            logger.info("SMS response: {} {}".format(headers, response.content))
            response_json = json.loads(response.content)
        except ValueError as error:
            logger.exception(f"{error}")
            return ""

        if response.status_code == 200 and response_json.get("type", "") == "success":
            logger.info("Message sent to phone={}, {} response : {}".format(
                mobile, otp, response.content))
            return otp
        else:
            logger.debug("Unable to send message to phone={}, response : {}".format(
                mobile, response.content))
            return ""

    def verify(self, mobile, otp):
        url = BASE_URL + f"/otp/verify?otp={otp}&mobile={mobile}"
        headers = {
            'accept': 'application/json',
            'authkey': AUTH_KEY
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps({}))
            logger.info("SMS response: {}".format(response.content))
            response_json = json.loads(response.content)
        except ValueError as error:
            logger.exception(f"{error}")
            return False

        if response.status_code == 200 and response_json.get("type", "") == "success":
            logger.info("OTP verified successfully phone={}, response : {}".format(
                mobile, response.content))
            return True
        else:
            logger.info("Unable to verify otp. phone={}, response : {}".format(
                mobile, response.content))
            return False

    def send_sms(self, mobile, msg, msg2):
        payload = {
            "template_id": TEMPLATE_ID,
            "sender": SENDER_ID,
            "short_url": "0",
            "mobiles": self.format_mobile(mobile),
            "VAR1": msg,
            "VAR2": msg2
        }

        headers = {
            'Authkey': AUTH_KEY,
            'accept': "application/json",
            'content-type': "application/json"
        }

        url = BASE_URL + "/flow/"
        try:
            requests.post(url, data=payload, headers=headers)
        except Exception as e:
            logger.exception(f"MSG91 Server Error: {e}")
            return
        return
