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


####################################反序列化(JSON,字典 转换为 对象(模型))  数据的校验#########################################

"""
数据的校验有5中形式:

第一种验证:
    我们的字段的类型 进行校验,我们传递的数据的类型,必须满足 字段的类型要求

第二种验证:
    字段选项:
        max_length: 字符串的最大长度        char
        min_length: 字符串的最小长度
        max_value:     最大值                 int
        min_value:      最小值
        required	表明该字段在反序列化时必须输入，默认True
        default     默认值

第三种方式: 当我们的类型和选项都满足条件之后,我们需要对单个字段的值进行校验,我们在序列化器中实现方法
        以 validate_ 开头 以 字段名结尾的函数

        def validate_fieldsname(self,value):

            return value


第四种方式:
    对多个字段进行校验的时候,我们在序列器中实现
    def validate(self,attrs)

        return attrs

第五种方式:
    自定义验证器


"""

####################################反序列化(JSON,字典 转换为 对象(模型))  数据的入库#########################################

from book.serializers import BookInfoSerializer

# 1.接收数据
data = {
    'name':'python',
    'pub_date':'2000-1-1',
    # 'pub_date':'20',
    # 'readcount':-1,
    'readcount':10000,
    'commentcount':100,
    'is_delete':0
}

# 2.对数据进行校验 -- > 序列化器 : 创建序列化器
# Serializer 的第一个参数是: instance  对象
# Serializer 的第二个参数是: data       要校验(入库)的数据
serializer = BookInfoSerializer(data=data)

#需要调用序列化器的 is_valid方法进行校验
# 如果数据没有问题,则返回True
# 如果数据有问题,则返回False
# serializer.is_valid()

# serializer.is_valid()
# raise_exception 如果有错误则抛出异常
serializer.is_valid(raise_exception=True)

#3. 入库 调用序列化器的 save方法
serializer.save()

"""
评论量不能大于阅读量的测试结果如下：
(django_py3_1.11) python@ubuntu:~/PycharmProjects/Django code/bookmanager04$ python manage.py shell
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from book.serializers import BookInfoSerializer
>>>
>>> # 1.接收数据
>>> data = {
...     'name':'python',
...     'pub_date':'2000-1-1',
...     # 'pub_date':'20',
...     # 'readcount':-1,
...     'readcount':10,
...     'commentcount':100,
...     'is_delete':0
... }
>>>
>>> # 2.对数据进行校验 -- > 序列化器 : 创建序列化器
>>> # Serializer 的第一个参数是: instance  对象
>>> # Serializer 的第二个参数是: data       要校验(入库)的数据
>>> serializer = BookInfoSerializer(data=data)
>>>
>>> #需要调用序列化器的 is_valid方法进行校验
>>> # 如果数据没有问题,则返回True
>>> # 如果数据有问题,则返回False
>>> # serializer.is_valid()
>>>
>>> # serializer.is_valid()
>>> # raise_exception 如果有错误则抛出异常
>>> serializer.is_valid(raise_exception=True)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/python/.virtualenvs/django_py3_1.11/lib/python3.5/site-packages/rest_framework/serializers.py", line 244, in is_valid
    raise ValidationError(self.errors)
rest_framework.exceptions.ValidationError: {'non_field_errors': [ErrorDetail(string='评论量不能大于阅读量', code='invalid')]}
"""

"""
#3. 入库 调用序列化器的 save方法

serializer.save() 入库的时候出现这个错误：
NotImplementedError: `create()` must be implemented.

原因在于：
serializer.save() 继承自serializers.Serializer的序列化器，
在调用save方法的时候，
需要手动实现create方法。

(其中serializers.Serializer来自这句话
from book.serializers import BookInfoSerializer,
BookInfoSerializer的父类便是serializers.Serializer)

"""

####################################反序列化(JSON,字典 转换为 对象(模型))  数据的更新#########################################


from book.serializers import BookInfoSerializer
from book.models import BookInfo

book = BookInfo.objects.get(id=1)

# 1.接收数据
data = {
    'name':'射雕英雄前传0--之缅怀金庸',
    'pub_date':'2010-1-1',
    'readcount':100399,
    'commentcount':666
}

# 序列化器 有2个参数:
# 第一个参数是: instance      对象
# 第二个参数是: data          校验的数据
# 如果我们传递了 instance 和 data 2个数据,则系统认为我们在进行 更新操作
serializer = BookInfoSerializer(instance=book,data=data)

# 调用save之前 ,必须调用 is_valid
serializer.is_valid(raise_exception=True)

# 保存(更新)一下 都是调用 save方法
serializer.save()

"""

出现这个错误：
NotImplementedError: `update()` must be implemented.

原因在于：
serializer.save() 继承自serializers.Serializer的序列化器，
在进行更新操作，调用save方法的时候，
需要手动实现update方法。

"""