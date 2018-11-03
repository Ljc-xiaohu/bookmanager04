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

        # # 2.将对象列表转换为字典列表
        # lists = []
        # for book in books:
        #     lists.append({
        #         'id': book.id,
        #         'name': book.name,
        #         'pub_date': book.pub_date,
        #         'readcount': book.readcount
        #     })
        #
        # # 3.返回响应
        # return JsonResponse(lists, safe=False)

        # 使用序列化器(等价与上面 2.将对象列表转换为字典列表&3.返回响应 的代码)
        serializer = BookInfoSerializer(books,many=True)

        return JsonResponse(serializer.data,safe=False)

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


############################## 序列化器 ################################

from book.models import BookInfo
from book.serializers import BookInfoSerializer

# 1.获取对象
book = BookInfo.objects.get(id=1)

# 2.创建序列化器(序列化器可以将对象 转换为 字典)
# 序列化器的 第一个参数是： instance 实例对象，下面2行代码等价
serializer = BookInfoSerializer(instance=book)
# serializer = BookInfoSerializer(book)

# 3.获取字典数据,终端中回车后便可得到结果
serializer.data

"""
终端运行结果：
(django_py3_1.11) python@ubuntu:~/PycharmProjects/Django code/bookmanager04$ python manage.py shell
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from book.models import BookInfo
>>> from book.serializers import BookInfoSerializer
>>>
>>> # 1.获取对象
>>> book = BookInfo.objects.get(id=1)
>>> # 2.创建序列化器(序列化器可以将对象 转换为 字典)
>>> # 序列化器的 第一个参数是： instance 实例对象
>>> serializer = BookInfoSerializer(instance=book)
>>>
>>> # 3.获取字典数据
>>> serializer.data
{'readcount': 12, 'id': 1, 'name': '射雕英雄后传', 'is_delete': False, 'commentcount': 34, 'pub_date': '1980-05-01'}

"""

####################################对象列表##########################################
from book.models import BookInfo
from book.serializers import BookInfoSerializer

#1. 获取对象列表
books = BookInfo.objects.all()

# 2.创建序列化器
# 如果要被序列化的是包含多条数据的查询集QuerySet，可以通过添加many=True参数补充说明
serializer = BookInfoSerializer(books,many=True)

#3. 获取转换之后的字典
serializer.data

# 之后便可以使用 JsonResponse(serializer.data)，返回json

"""
Ordered     Dict  本质是字典,只不过这个字典有顺序,结果如下：
[
OrderedDict([('id', 1), ('name', '射雕英雄后传'), ('pub_date', '1980-05-01'), ('readcount', 12), ('commentcount', 34), ('is_delete', False)]),
OrderedDict([('id', 2), ('name', '天龙八部'), ('pub_date', '1986-07-24'), ('readcount', 36), ('commentt', 40), ('is_delete', False)]),
OrderedDict([('id', 3), ('name', '笑傲江湖'), ('pub_date', '1995-12-24'), ('readcount',, ('commentcount', 80), ('is_delete', False)]),
OrderedDict([('id', 4), ('name', '雪山飞狐'), ('pub_date', '1987-11-11')readcount', 58), ('commentcount', 24), ('is_delete', False)])
]

"""


####################################外键##########################################

from book.models import PeopleInfo
from book.serializers import PeopleInfoSerializer

#1.获取对象
person = PeopleInfo.objects.get(id=1)

#2.创建序列化器
serializer = PeopleInfoSerializer(person)

#3.获取字典
serializer.data

"""
{
'book': OrderedDict([('id', 1), ('name', '射雕英雄后传'), ('pub_date', '1980-05-01'), ('readcount', 12), ('commentcount', 34), ('is_delete', False)]),
'id': 1,
'description': '降龙十八掌',
'gender': 1,
'name': '郭靖'
}
"""