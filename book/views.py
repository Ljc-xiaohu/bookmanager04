from django.http import HttpResponse
from django.shortcuts import render

from book.models import BookInfo
from book.serializers import BookModelSerializer

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


#以书籍列表视图为例 完成我们代码
class BookListAPIView(APIView):

    #获取所有书籍
    def get(self,request):
        """
        1.获取模型列表
        2.我们创建序列化器,让序列化器对我们的模型列表转换
        3.返回响应
        """
        # 1.获取模型列表
        books = BookInfo.objects.all()

        # 2.我们创建序列化器,让序列化器对我们的模型列表转换
        serializer = BookModelSerializer(books,many=True)

        # 3.返回响应
        return  Response(serializer.data)


    #新增书籍
    def post(self,request):
        """
         # 1.接收数据
        # 2.校验数据
        # 3.创建对象，保存到数据库
        # 4.返回响应
        """
        # 1.接收数据
        data = request.data

        # 2.校验数据,我们用序列化器
        serializer = BookModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 3.创建对象，保存到数据库
        serializer.save()

        # 4.返回响应
        return Response(serializer.data)


#详情视图



###########################二级视图GenericAPIView##############################################
from rest_framework.generics import GenericAPIView

"""
为标准列表和详细信息视图添加了常用的行为。

提供的每个具体通用视图是通过GenericAPIView与一个或多个mixin类组合而构建的


1. GenericAPIView 对列表视图和详情视图做了 通用的 支持, 在APIView的基础之上 做了 属性和方法的封装

    属性
    queryset                用于记录我们列表,详情视图的查询结果集
    serializer_class        用于列表,详情视图的序列化器
    lookup_field            用于查询指定的对象的字段名,默认是 pk

    方法
    get_queryset            用于获取查询的结果(本质是: queryset.all())
    get_serializer          用于获取序列化器(本质是: serializer_class())
    get_object              用于获取某一个指定的对象(本质是: 根据 lookup_field的字段的值,进行筛选)
"""

#书籍列表视图
class BookListGenericAPIView(GenericAPIView):

    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    #获取所有的书籍
    def get(self,request):
        """
         1.获取模型列表
        2.我们创建序列化器,让序列化器对我们的模型列表转换
        3.返回响应
        """
        #  1.获取模型列表
        # books = self.queryset.all()
        books = self.get_queryset()

        # 2.我们创建序列化器,让序列化器对我们的模型列表转换
        # serializer = self.serializer_class(books,many=True)
        serializer = self.get_serializer(books,many=True)

        # 3.返回响应
        return Response(serializer.data)

    def post(self,request):
        """
        # 1.接收数据
        # 2.校验数据
        # 3.创建对象，保存到数据库
        # 4.返回响应
        """
        # 1.接收数据
        data = request.data

        # 2.校验数据,序列化器
        # self.get_serializer() = BookSerializer()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 3.创建对象，保存到数据库
        serializer.save()

        # 4.返回响应
        return Response(serializer.data)