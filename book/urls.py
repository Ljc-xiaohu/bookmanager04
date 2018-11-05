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
    url(r'^books/$', views.BookViewSet.as_view({'get': 'list'})),
    url(r'^books/(?P<pk>\d+)/$', views.BookViewSet.as_view({'get': 'retrieve'})),
]

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
#
# router.register(r'booklist',views.BookModelViewSet,base_name='')
#
# urlpatterns += router.urls
