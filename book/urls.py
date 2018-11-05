from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^index/$', views.IndexView.as_view()),
    #
    # # 定义列表视图的url
    # url(r'^books/$', views.BookView.as_view()),
    #
    # # 定义详情视图的url
    # url(r'^books/(?P<id>\d+)/$',views.BookDetailView.as_view()),

    # url(r'^centers/$',views.CenterView.as_view()),

    # # 列表视图
    # url(r'^books/$',views.BookListAPIView.as_view()),

    # 列表视图
    # url(r'^books/$',views.BookListGenericAPIView.as_view()),
    # url(r'^books/$',views.BookListGenericMixinView.as_view()),

    # url(r'^books/$',views.BookCreateAPIView.as_view()),

    # 详情视图
    # url(r'^books/(?P<id>\d+)/$',views.BookDetailGeneicAPIView.as_view()),
    # url(r'^books/(?P<pk>\d+)/$',views.BookDetailGenericMixinView.as_view()),

    # 视图集
    # url(r'^books/$', views.BookViewSet.as_view({'get': 'list'})),
    # url(r'^books/(?P<pk>\d+)/$', views.BookViewSet.as_view({'get': 'retrieve'})),
]

"""
    1. 视图集是采用 Router自动生成url, 自动生成2个url 一个是列表视图,一个是详情视图

    2. DefaultRouter,SimpleRouter 的共同点: 生成url
     DefaultRouter,SimpleRouter 的不同点:
     DefaultRouter, http://127.0.0.1:8000/ 可以访问
     SimpleRouter，http://127.0.0.1:8000/   不可以访问，
     只能通过
     ^ ^books/$ [name='-list']
     ^ ^books/(?P<pk>[^/.]+)/$ [name='-detail']
     例如：
     http://127.0.0.1:8000/books/
     http://127.0.0.1:8000/books/1/

"""
from rest_framework.routers import DefaultRouter,SimpleRouter

# 1.创建 router对象
# router = DefaultRouter()
router = SimpleRouter()

#2.需要让router注册 url
# register 有三个参数
# 参数1: 正则, 正则的值 是 列表视图和详情视图的公共部分,不包括 /
# abc/
# abc/pk/
#参数2: 视图集
#参数3: 视图函数名的前缀:  列表视图的名字是:  base_name -list
#                       详情视图的名字是:  base_name -detail
router.register(r'books',views.BookModelViewSet,base_name='')

#3. router会自动生成url,生成的url在 router.urls属性中
# 将url 添加到 urlpatterns
urlpatterns += router.urls


"""
router.register(r'books',views.BookModelViewSet,base_name='book'),其中的base_name='book'表示：

^ ^books/$ [name='book-list']
^ ^books/(?P<pk>[^/.]+)/$ [name='book-detail']

访问结果如下
Page not found (404)
Request Method:	GET
Request URL:	http://127.0.0.1:8000/
Using the URLconf defined in bookmanager04.urls, Django tried these URL patterns, in this order:

^admin/
^ ^books/$ [name='book-list']
^ ^books/(?P<pk>[^/.]+)/$ [name='book-detail']

若base_name=''，则结果如下
^admin/
^ ^books/$ [name='-list']
^ ^books/(?P<pk>[^/.]+)/$ [name='-detail']
"""