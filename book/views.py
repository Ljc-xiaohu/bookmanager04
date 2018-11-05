from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from book.models import BookInfo
from book.serializers import BookModelSerializer

"""
    认证一般和权限配合使用

"""


from rest_framework.pagination import PageNumberPagination
class CustomNumberPagination(PageNumberPagination):
    #我们需要设置一个默认值 来开启分页
    page_size = 10

    # 我们需要设置一个 查询的key 来开启 每页多少条
    page_size_query_param = 'page_size'

    page_query_param = 'pn'   #前端url中的 key ,默认是 page


# BookModelViewSet 所有人都可以访问
class BookModelViewSet(ModelViewSet):
    # ModelViewSet 父类是 GenericAPIView
    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
    permission_classes = [AllowAny]

    # throttle_scope = 'contacts'  # 限制用户对于每个视图的访问频次

    # 过滤
    filter_fields = ['name','id','readcount']

    # http://127.0.0.1:8000/admin/book/bookinfo/?name=python


    from rest_framework.filters import OrderingFilter
    #设置过滤的后台为 排序
    filter_backends = [OrderingFilter]
    # 排序的字段列表
    ordering_fileds = ['id','readcount','commentcount']

    # http://127.0.0.1:8000/books/?ordering=readcount   # 默认为升序
    #  http://127.0.0.1:8000/books/?ordering=-readcount   # 加一个 - 表示降序


    # 分页的第一点:  GenericAPIView及其子类有分页功能 ,APIView没有分页功能
    from rest_framework.generics import GenericAPIView

    # 分页有2个分页类
    from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

    # 也可通过自定义Pagination类，来为视图添加不同分页行为。在视图中通过pagination_clas属性来指明
    # pagination_class = LimitOffsetPagination

    pagination_class = CustomNumberPagination

"""
class LimitOffsetPagination(BasePagination): (其中部分源码，可以自己查看)

    default_limit = api_settings.PAGE_SIZE
    limit_query_param = 'limit'     # 表示：  每页限制数量
    limit_query_description = _('Number of results to return per page.')
    offset_query_param = 'offset'   # 表示：  初始索引
    offset_query_description = _('The initial index from which to return the results.')
"""


# CenterAPIView 我想用于测试, BasicAuthentication
# 可以对这个视图 采用单独的认证方案
# 视图的设置 优先于 settings中的认证
from rest_framework.authentication import BasicAuthentication
class CenterAPIView(APIView):

    authentication_classes = (BasicAuthentication,)
    # authentication_classes = [BasicAuthentication]

    def get(self,request):
        pass


