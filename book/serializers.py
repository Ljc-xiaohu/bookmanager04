from rest_framework import serializers

# 将模型转换为JOSN, 将JSON转换Wie对象(模型),验证
from book.models import BookInfo


class BookModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookInfo
        fields = '__all__'