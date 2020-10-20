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
        keys_field_blank = [key for key, value in response.data.items() if value == "This field may not be blank."]
        error_message = ""
        # print(keys_field_blank)
        if keys_field_blank:
            error_message += 'Some required fields are blank: ' + ', '.join(keys_field_blank)+'\n'
        for key, value in response.data.items():
            if key not in keys_field_blank:
                for val in value:
                    # print(key, val)
                    if key == "non_field_errors":
                        error_message += f"{val.strip('.')}\n"
                    # elif "blank" in val or "required" in val:
                    #     print(val)
                    else:
                        error_message += f"{val.strip('.')}: {key}\n"
        response.data = {'error_message': error_message}
    if isinstance(exc, exceptions.NotFound) or isinstance(exc, Http404):
        # pprint(response.data)
        response.data = {'error_message': 'Resources not found.'}
    if isinstance(exc, exceptions.PermissionDenied):
        # pprint("Permission Denied" + response.data)
        response.data = {'error_message': 'You are not allowed to do this action.'}
    return response