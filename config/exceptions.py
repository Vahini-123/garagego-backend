from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default handler so every error response has the same shape:
    { "error": true, "detail": <str or dict>, "status_code": <int> }
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "error": True,
            "detail": response.data,
            "status_code": response.status_code,
        }

    return response
