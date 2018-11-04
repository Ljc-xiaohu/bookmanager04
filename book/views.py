from django.http import HttpResponse
from django.shortcuts import render

"""
1.我们学习 DRF框架的视图的基类是 APIVIew
2. APIView的使用 和View是一样的
3. APIView中的 请求和响应是不一样的

    1）data
    request.data返回解析之后的请求体数据。
    类似于Django中标准的request.POST属性，但提供如下特性：
    包含了对POST、PUT、PATCH请求方式解析后的数据
    利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据

    2）query_params
    request.query_params与Django标准的request.GET相同，只是更换了更正确的名称而已。
"""
from rest_framework.views import APIView
from rest_framework.request import Request

class CenterView(APIView):

    def get(self, request):

        # request.GET
        query_params = request.query_params
        print(query_params)

        return HttpResponse('get')

    def post(self, request):

        # request.POST  request.body
        data = request.data
        print(data)

        return HttpResponse('post')
