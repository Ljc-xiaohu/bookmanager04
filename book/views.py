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


# 书籍详情视图
class BookDetailGeneicAPIView(GenericAPIView):

    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    #设置 查询的字段,默认 lookup_field = pk
    lookup_field = 'id'


    def get(self,request,id):
        """
        # 1.根据id获取对象
        #2.创建序列化器
        # 3.返回响应
        """
        # 1.根据id获取对象
        book = self.get_object()

        #2.创建序列化器
        serializer = self.get_serializer(book)

        # 3.返回响应
        return Response(serializer.data)


    def put(self,request,id):
        """
        1.根据id获取对象
        2.接收参数
        3.校验参数
        4.更新操作
        5.返回响应
        """
        #  1.根据id获取对象
        book = self.get_object()

        # 2.接收参数
        # 3.校验参数  --序列化器
        serializer = self.get_serializer(instance=book,data=request.data)
        serializer.is_valid()

        # 4.更新操作
        serializer.save()

        # 5.返回响应
        return  Response(serializer.data)


    def delete(self,request,id):
        """
        1.根据id查询对象
        2.删除
        3.返回响应
        """
        # 1.根据id查询对象
        book = self.get_object()

        # 2.删除
        book.delete()

        # 3.返回响应
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)


###########################二级视图GenericAPIView 一般和 MiXin配合使用##############################################

from rest_framework.mixins import ListModelMixin,CreateModelMixin

#列表视图
class BookListGenericMixinView(ListModelMixin,CreateModelMixin,GenericAPIView):

    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    def get(self,request):

        return self.list(request)

    def post(self,requset):

        return self.create(requset)


#详情视图
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin

class BookDetailGenericMixinView(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):

    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    def get(self,request,pk):

        return self.retrieve(request)

    def put(self,request,pk):

        return self.update(request)

    def delete(self,request,pk):

        return self.destroy(request)


###########################三级视图##############################################

"""

queryset
- 应该用于从此视图返回对象的查询集。通常，您必须设置此属性，或覆盖该get_queryset()方法。
如果要覆盖视图方法，则必须调用get_queryset()而不是直接访问此属性，因为queryset将进行一次评估，
并且将为所有后续请求缓存这些结果。

serializer_class
- 应该用于验证和反序列化输入以及序列化输出的序列化程序类。通常，您必须设置此属性，
或覆盖该get_serializer_class()方法。

"""


from rest_framework.generics import CreateAPIView

class BookCreateAPIView(CreateAPIView):

    # queryset = BookInfo.objects.all()

    def get_queryset(self):

        return BookInfo.objects.all()

    # serializer_class = BookModelSerializer

    def get_serializer_class(self):

        return BookModelSerializer


###########################视图集##############################################

"""

Django REST框架允许将一组相关视图的逻辑组合到一个类中，称为  视图集
# 我们需要将 列表视图和详情视图 合并到一个 视图集(View)中
# 但是 一个View只能有一个 get方法, 那 视图集

视图集的 爷爷类 是一个 View

"""

from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class BookViewSet(ViewSet):

    def list(self,request):                 #GET
        queryset = BookInfo.objects.all()
        serializer = BookModelSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):     #GET
        queryset = BookInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookModelSerializer(user)
        return Response(serializer.data)
