import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from book.models import BookInfo


class IndexView(View):
    def get(self, request):
        return HttpResponse('ok')


"""
Restfull风格的图书管理系统

# 列表视图
获取所有书籍          GET         books/
新增书籍             POST         books/

#详情视图
获取一本书籍          GET         books/id/
修改一本书籍          PUT         books/id/
删除一本书籍          DELETE      books/id/
"""


# 列表视图
class BookView(View):
    # 获取所有书籍
    def get(self, request):
        """
        1.查询所有书籍 []
        2.将对象列表转换为字典列表
        3.返回响应
        """
        # 1.查询所有书籍 []
        books = BookInfo.objects.all()
        # [BookInfo,BOokInfo,]

        # 2.将对象列表转换为字典列表
        lists = []
        for book in books:
            lists.append({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date,
                'readcount': book.readcount
            })

        # 3.返回响应
        return JsonResponse(lists, safe=False)

    # 新增书籍
    def post(self, request):
        """
        1.接收数据
        2.校验数据
        3.创建对象，保存到数据库
        4.返回响应
        """
        # 1.接收数据
        body = request.body
        body_str = body.decode()  # 解码成json类型的字符串
        params = json.loads(body_str)  # 将字符串转换为字典

        # 2.校验数据(校验省略)
        # 3.创建对象，保存到数据库
        book = BookInfo.objects.create(
            name=params.get('name'),
            pub_date=params.get('pub_date'),
            readcount=params.get('readcount')
        )

        # 4.返回响应
        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount
        })


# 详情视图
class BookDetailView(View):
    def get(self, request, id):
        """
        1.根据id获取对象
        2.返回响应
        """
        # 1.根据id获取对象
        try:
            book = BookInfo.objects.get(id=id)
        except BookInfo.DoesNotExist:
            # status=400表示：INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
            return HttpResponse(status=400)

        # 2.返回响应
        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount
        })

    # 修改某一本书籍
    def put(self, request, id):
        """
        1.根据id获取对象
        2.接收参数
        3.校验参数
        4.更新操作
        5.返回响应
        """
        # 1.根据id获取对象
        try:
            book = BookInfo.objects.get(id=id)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=400)

        # 2.接收参数
        params = json.loads(request.body.decode())

        # 3.校验参数(省略)
        # 4.更新操作
        book.name = params.get('name', book.name)
        book.pub_date = params.get('pub_date', book.pub_date)
        book.readcount = params.get('readcount', book.readcount)
        book.save()

        # 5.返回响应
        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount
        })

    def delete(self, request, id):
        """
        1.根据id查询对象
        2.删除
        3.返回响应
        """
        # 1.根据id查询对象
        try:
            book = BookInfo.objects.get(id=id)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=400)

        # 2.删除
        book.delete()

        # 3.返回响应
        return HttpResponse(status=204)  # NO CONTENT - [DELETE]：用户删除数据成功。

"""
    JSON --> 模型(对象)             :反序列化
    模型(对象) --> JSON(字典)         :序列化
"""
from  rest_framework.viewsets import ModelViewSet
from .serializers import BookModelSerializer
class BookModelViewSet(ModelViewSet):

    serializer_class = BookModelSerializer

    queryset = BookInfo.objects.all()