from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    Throttled,
    AuthenticationFailed,
    NotAuthenticated,
    MethodNotAllowed,
    ParseError,
)
from rest_framework.response import Response
import logging

logger = logging.getLogger("default")
# Custom Exception
def custom_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)

        if isinstance(exc, Throttled):
            custom_response_data = {"message": "Request limit exceeded"}
            response.data = custom_response_data

        elif isinstance(exc, AuthenticationFailed) or isinstance(exc, NotAuthenticated):
            custom_response_data = {
                "message": "Authentication credentials were not provided"
            }
            response.data = custom_response_data

        elif isinstance(exc, MethodNotAllowed):
            custom_response_data = {"message": "Method not allowed"}
            response.data = custom_response_data

        elif isinstance(exc, ParseError):
            custom_response_data = {"message": exc.detail}
            response.data = custom_response_data
        elif (
            isinstance(exc, Exception) and getattr(exc, "status_code", None) is None
        ):  # not restframework's exception
            response = Response(
                {"message": "INTERNAL SERVER ERROR", "trace": str(exc)}, status=500
            )
            logger.exception(exc)
        else:
            logger.error(response.data)
        logger.exception(exc)
        return response
    except Exception as e:
        logger.exception(e)
        response = Response(
            {"message": "INTERNAL SERVER ERROR", "trace": str(e)}, status=500
        )
        return response
