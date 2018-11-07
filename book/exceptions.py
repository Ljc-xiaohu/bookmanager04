from rest_framework.views import exception_handler
from rest_framework import status
from django.db import DatabaseError
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # exc 当前异常的对象
    # context 哪个地方出的问题

    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)
    # 在此处补充自定义的异常处理
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
