from django.http import HttpResponse
from django.shortcuts import render

"""
1.我们学习 DRF框架的视图的基类是 APIVIew
2. APIView的使用 和View是一样的
3. APIView中的 请求和响应是不一样的

请求：
    1）data
    request.data返回解析之后的请求体数据。
    类似于Django中标准的request.POST属性，但提供如下特性：
    包含了对POST、PUT、PATCH请求方式解析后的数据
    利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据

    2）query_params
    request.query_params与Django标准的request.GET相同，只是更换了更正确的名称而已。

响应：
    REST framework提供了Renderer渲染器，用来根据请求头中的Accept（接收数据类型声明）来自动转换响应数据到对应格式。
    如果前端请求中未进行Accept声明，则会采用默认方式处理响应数据，我们可以通过配置来修改默认响应格式。

"""
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

class CenterView(APIView):

    def get(self, request):

        # request.GET
        query_params = request.query_params
        print(query_params)

        dict = {
            'name':'阿三'
        }
        from rest_framework import status
        return Response(dict,status=status.HTTP_201_CREATED)

        return Response(dict, status=201)

        return HttpResponse('get')
        return JsonResponse({})

    def post(self, request):

        # request.POST  request.body
        data = request.data
        print(data)

        return HttpResponse('post')
