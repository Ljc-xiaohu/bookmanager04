from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


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
    def get(self, request):
        pass

    def post(self, request):
        pass


# 详情视图
class BookDetailView(View):
    def get(self, request, id):
        pass

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass
