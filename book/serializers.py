from rest_framework import serializers

# 将模型转换为JOSN, 将JSON转换Wie对象(模型),验证
from book.models import BookInfo

# ModelSerializer
#               1.自动帮我们生成 序列化器字段
#               2.自动实现了 update方法和create方法

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        #我们必须要关联模型
        model = BookInfo
        # 设置哪些字段可以生成 序列化器字段
        # fields = '__all__'      # __all__ 表示模型的所有字段
        # fields = ['id','name','pub_date']      # 设置部分字段

        exclude = ['image', 'is_delete']  # 抛出列表所罗列的,剩余的字段

        """
        {
        'id': 1,
        'pub_date': '2010-01-01',
        'name': '射雕英雄前传0--之缅怀金庸',
        'commentcount': 666,
        'readcount': 100399
        }
        """

        """
        ModelSerializer与常规的Serializer相同，但提供了：

        基于模型类自动生成一系列字段

        包含默认的create()和update()的实现
        """

        """
        基于模型类自动生成一系列字段:
        >>> s
        BookModelSerializer(data={'name': '听说下雨天吃巧克力更配哦', 'pub_date': '2010-1-1', 'readcount': 100399, 'commentcount': 666}):
            id = IntegerField(label='ID', read_only=True)
            name = CharField(label='名称', max_length=20)
            pub_date = DateField(allow_null=True, label='发布日期', required=False)
            readcount = IntegerField(label='阅读量', max_value=2147483647, min_value=-2147483648, required=False)
            commentcount = IntegerField(label='评论量', max_value=2147483647, min_value=-2147483648, required=False)

        """

        # 可以通过read_only_fields指明只读字段，即仅用于序列化输出的字段
        read_only_fields = ['readcount', 'commentcount']

        # 我们可以使用extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
        # 修改 默认生成在 字段的选项
        extra_kwargs = {
            #  '字段名':{'选项名':值}
            'pub_date': {'required': True},
            'readcount': {
                'max_value': 100,
                'min_value': 1
            }
        }

        """
        使用read_only_fields和extra_kwargs方法之后：
        >>> s
        BookModelSerializer(data={'readcount': 100399, 'pub_date': '2010-1-1', 'name': '听说下雨天吃巧克力更配哦', 'commentcount': 666}):
            id = IntegerField(label='ID', read_only=True)
            name = CharField(label='名称', max_length=20)
            pub_date = DateField(allow_null=True, label='发布日期', required=True)
            readcount = IntegerField(label='阅读量', max_value=100, min_value=1, read_only=True)
            commentcount = IntegerField(label='评论量', read_only=True)
        >>>

        """


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

    # 第五种方式:自定义验证器,custom_validate,自定义的名字
    def custom_validate(self):
        # if self == 'admin':
        #     raise serializers.ValidationError('admin不可用')
        raise serializers.ValidationError('我就是来捣乱的')

    id = serializers.IntegerField(read_only=True,label='id')  # label 表示注释
    # name = serializers.CharField(max_length=20,label='名字',required=True,validators=[custom_validate])
    name = serializers.CharField(max_length=20,label='名字',required=True)
    pub_date = serializers.DateField(label='发布日期',required=True)
    # 其中required=True时,不能设置default的值
    readcount = serializers.IntegerField(label='阅读量',required=True)
    commentcount = serializers.IntegerField(required=False)
    is_delete = serializers.BooleanField(required=False,default=False)

    # 1本书对应多个人物 ,我们就是要获取人物的信息,不能修改，read_only=True
    #
    # peopleinfo_set = serializers.PrimaryKeyRelatedField(read_only=True)  # 缺少 many=True
    peopleinfo_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)

    # 少写一个
    # image = serializers.ImageField()

    # 对应views中的第三种方式
    def validate_readcount(self, value):

        if value < 0:
            raise serializers.ValidationError('阅读量不能为负数')

        # 验证完成之后,需要将 value返回
        return value

    # 下面2行代码等价
    # def validate(self, attrs):
    def validate(self, data):
        # attrs = data
        # params --> 序列化器data --> attrs
        """
        data = {
            'name':'python',
            'pub_date':'2000-1-1',
            'readcount':10,
            'commentcount':100
        }
        """
        readcount = data.get('readcount')
        # if readcount<0:
        #     raise serializers.ValidationError()
        commentcount = data.get('commentcount')
        if readcount < commentcount:
            raise serializers.ValidationError('评论量不能大于阅读量')

        #校验完成之后,必须要将数据返回回去
        return data

    def create(self, validated_data):
        # validated_data 验证之后的数据
        # params(前端提交的数据) --> data(序列器接受的数据) --> attrs(多个字段校验) --> validated_data(校验之后)
        # 如果前段提交的数据 经过序列化器的验证之后完全满足需求,则
        # validated_data =  params
        """

        validated_data:
        data = {
            'name':'python',
            'pub_date':'2000-1-1',
            'readcount':10000,
            'commentcount':100
        }
        """
        # book = BookInfo()
        # book.save()

        # create(**kwargs),中需要传入一个key，value的字典类型，
        # 所以需要对validated_data进行解包，便是**validated_data
        book = BookInfo.objects.create(**validated_data)

        # 需要将创建的对象 返回
        return book

    def update(self, instance, validated_data):
        # instance,          传递过来的对象
        # validated_data    验证之后的数据

        instance.name = validated_data.get('name',instance.name)
        instance.pub_date = validated_data.get('pub_date',instance.pub_date)
        instance.readcount = validated_data.get('readcount',instance.readcount)
        instance.commentcount = validated_data.get('commentcount',instance.commentcount)

        # 对实例对象进行保存
        instance.save()

        #最终要返回对象
        return instance


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