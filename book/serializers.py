from rest_framework import serializers

# 将模型转换为JOSN, 将JSON转换Wie对象(模型),验证
from book.models import BookInfo


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'


# DRF魅力的时候 我们所做的
#   将对象(模型)转换为字典,JSON ,
# 将字典,JSON 转换为对象(模型)
#  数据的验证


# 以上三个事情  序列化器(Serializer) 都可以实现


# Serializer
# Django文档
# Serializer字段处理    原始值和内部数据类型之间的转换。    它们还处理验证输入值

#   原始值(JSON,字典,XML)和内部数据(模型,对象)类型之间的转换

#   模型(对象) -->  JSON,字典,XML
#   JSON,字典,XML  -->   (数据进行验证)     -->模型(对象)
#   处理验证输入值


# 模型(对象) -->  字典 ({key:value,...})

class BookInfoSerializer(serializers.Serializer):
    """
    1.序列化器的 (暂时)字段名 要和 模型名一致
    2.类型, 类型和模型的类型一致
    3.选项:
        read_only = True 表示只读
    """
    id = serializers.IntegerField(read_only=True,label='id')  # label 表示注释
    name = serializers.CharField(max_length=20,label='名字')
    pub_date = serializers.DateField(label='发布日期')
    readcount = serializers.IntegerField(label='阅读量')
    commentcount = serializers.IntegerField()
    is_delete = serializers.BooleanField()

    # 少写一个
    # image = serializers.ImageField()