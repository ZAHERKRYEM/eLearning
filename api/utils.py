from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 401 and "token_not_valid" in response.data.get('code', ''):
            return Response({
                "status": False,
                "data": {},
                "message": "Token is invalid or expired.",
                "status_code": 401
            }, status=status.HTTP_401_UNAUTHORIZED)

    # إعادة الاستجابات الافتراضية إذا لم تكن خطأ التوكن
    return response
