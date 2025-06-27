from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status


def exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_msg = response.data

        if isinstance(error_msg, str):
            error_msg = {'detail': error_msg}
        elif not isinstance(error_msg, dict):
            error_msg = {'detail': 'An error occurred.'}

        error_msg = error_msg.get('detail', error_msg)

        return Response({
            'error': {
                'errorId': response.status_code,
                'errorMsg': error_msg
            },
            'success': False
        }, status=response.status_code)

    return Response({
        'error': {
            'errorId': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'errorMsg': "Internal server error."
        },
        'success': False
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def page_not_found_handler(request, exception=None):
    return JsonResponse({
        'error': {
            'errorId': status.HTTP_404_NOT_FOUND,
            'errorMsg': "Not found."
        },
        'success': False
    }, status=status.HTTP_404_NOT_FOUND)


def server_error_handler(request):
    return JsonResponse({
        'error': {
            'errorId': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'errorMsg': "Internal server error."
        },
        'success': False
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)