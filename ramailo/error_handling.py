"""Custom errors base and error handling."""

from abc import ABCMeta

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import set_rollback


class RamailoException(APIException, metaclass=ABCMeta):
    status_code = 400
    detail = "Ramailo Exception"

    def __init__(self, message, param=None):
        self.message = message
        self.param = param


def exception_to_error_type(exc):
    """Returns the type of an exception."""
    if isinstance(exc, exceptions.ValidationError):
        return "validation_error"

    if isinstance(exc, RamailoException):
        return exc.custom_error_type

    return "internal_error"


def custom_exception_handler(exc, context):
    """
    Returns a custom response that should be used for any given exception.
    By default we handle the REST framework `APIException` (`RamailoException`
    in particular), and also Django's built-in `Http404` and `PermissionDenied`
    exceptions. Any unhandled exceptions may return `None`, which will cause
    a 500 error to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}

        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        params = []

        if isinstance(exc, RamailoException):
            if exc.param is not None:
                params = [exc.param]
            messages = [exc.message]
        elif isinstance(exc.detail, list):
            messages = [", ".join(exc.detail)]
        elif isinstance(exc.detail, dict):
            params = list(exc.detail.keys())
            messages = [x for x in exc.detail.values()]
        else:
            messages = [exc.detail]

        data = {
            "status_code": exc.status_code,
            "type": exception_to_error_type(exc),
            "params": params,
            "messages": messages,
        }

        set_rollback()

        return Response(data, status=exc.status_code, headers=headers)

    return None
