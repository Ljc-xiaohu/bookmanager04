from rest_framework.viewsets import ModelViewSet
from rest_framework.views import  APIView
from book.models import BookInfo
from book.serializers import BookModelSerializer

"""
    认证一般和权限配合使用

"""

# BookModelViewSet 所有人都可以访问
class BookModelViewSet(ModelViewSet):
    # ModelViewSet 父类是 GenericAPIView
    queryset = BookInfo.objects.all()

    serializer_class = BookModelSerializer

    from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
    permission_classes = [AllowAny]




# CenterAPIView 我想用于测试, BasicAuthentication
# 可以对这个视图 采用单独的认证方案
# 视图的设置 优先于 settings中的认证
from rest_framework.authentication import BasicAuthentication
class CenterAPIView(APIView):

    authentication_classes = (BasicAuthentication,)
    # authentication_classes = [BasicAuthentication]

    def get(self,request):
        pass


