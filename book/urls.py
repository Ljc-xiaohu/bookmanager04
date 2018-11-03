from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index/$', views.IndexView.as_view()),

    # 定义列表视图的url
    url(r'^books/$', views.BookView.as_view()),

    # 定义详情视图的url
    url(r'^books/(?P<id>\d+)/$',views.BookDetailView.as_view()),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'booklist',views.BookModelViewSet,base_name='')

urlpatterns += router.urls
