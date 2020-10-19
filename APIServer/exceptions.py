from pprint import pprint

from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework import exceptions

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    pprint(response.data.keys())

    if isinstance(exc, exceptions.ValidationError):
        response.data = {'error_message': 'Some required fields are blank: ' + ', '.join(response.data.keys())}
    if isinstance(exc, exceptions.NotFound) or isinstance(exc, Http404):
        pprint(response.data)
        response.data = {'error_message': 'Resources not found.'}
    if isinstance(exc, exceptions.PermissionDenied):
        pprint(response.data)
        response.data = {'error_message': 'You are not allowed to do this action.'}
    return response