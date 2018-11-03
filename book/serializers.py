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
    name = serializers.CharField(max_length=20,label='名字',required=True)
    pub_date = serializers.DateField(label='发布日期',required=True)
    readcount = serializers.IntegerField(label='阅读量',required=False,default=1)
    commentcount = serializers.IntegerField(required=False)
    is_delete = serializers.BooleanField(required=False,default=False)

    # 1本书对应多个人物 ,我们就是要获取人物的信息,不能修改，read_only=True
    #
    # peopleinfo_set = serializers.PrimaryKeyRelatedField(read_only=True)  # 缺少 many=True
    peopleinfo_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)

    # 少写一个
    # image = serializers.ImageField()


class PeopleInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名字', max_length=20)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    description = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)

    #外键的设置
    #  PrimaryKeyRelatedField,此字段将被序列化为关联对象的主键
    # 人物所关联的外键 我们能修改吗? 是不能修改的 外键只能 读取 不能修改 read_only=True
    # book = serializers.PrimaryKeyRelatedField(read_only=True)
    # 或者 设置 queryset
    # 人物所关联的书籍 ,你把所有的书籍 返回给 queryset 系统会自动的获取它需要的值
    # book = serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())

    # StringRelatedField,此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    # 返回模型中的 __str__方法中的字符串内容
    # book = serializers.StringRelatedField()

    # 外键设置的第三方式,相当于嵌套了一个序列化器
    # book(dict) = BookInfoSerializer(book).data
    book = BookInfoSerializer()