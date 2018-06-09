# proposals/serializers.py

from rest_framework import serializers
from .models import Proposals,ProposalOptions,ProposalsCategory,ProposalsImage,Banner,HotSearchWords
from .models import ProposalsCategoryBrand,IndexAd
from django.db.models import Q

class CategorySerializer3(serializers.ModelSerializer):
    '''三级分类'''
    class Meta:
        model = ProposalsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    #在parent_category字段中定义的related_name="sub_cat"
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = ProposalsCategory
        fields = "__all__"

#商品分类
class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = ProposalsCategory
        fields = "__all__"

#轮播图
class ProposalsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalsImage
        fields = ("image",)

# 投票选项
class ProposalsOptionsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    # proposals = ProposalsSerializer()

    class Meta:
        model = ProposalOptions
        fields = '__all__'

# 投票列表页
class ProposalSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    category = CategorySerializer()
    class Meta:
        model = Proposals
        fields = '__all__'

#投票列表页
class ProposalsSerializer(serializers.ModelSerializer):
    #覆盖外键字段
    category = CategorySerializer()
    #images是数据库中设置的related_name="images"
    images = ProposalsImageSerializer(many=True)
    options = ProposalsOptionsSerializer(many=True)
    class Meta:
        model = Proposals
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    '''
    轮播图
    '''
    class Meta:
        model = Banner
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    '''
    大类下面的宣传商标
    '''
    class Meta:
        model = ProposalsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    #某个大类的商标，可以有多个商标，一对多的关系
    brands = BrandSerializer(many=True)
    # good有一个外键category，但这个外键指向的是三级类，直接反向通过外键category（三级类），取某个大类下面的商品是取不出来的
    proposals = serializers.SerializerMethodField()
    # 在parent_category字段中定义的related_name="sub_cat"
    # 取二级商品分类
    sub_cat = CategorySerializer2(many=True)
    # 广告商品
    ad_proposals = serializers.SerializerMethodField()

    def get_ad_proposals(self, obj):
        proposals_json = {}
        ad_proposals = IndexAd.objects.filter(category_id=obj.id, )
        if ad_proposals:
            #取到这个商品Queryset[0]
            good_ins = ad_proposals[0].proposals
            #在serializer里面调用serializer的话，就要添加一个参数context（上下文request）,嵌套serializer必须加
            # serializer返回的时候一定要加 “.data” ，这样才是json数据
            proposals_json = ProposalsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return proposals_json

    #自定义获取方法
    def get_proposals(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        all_proposals = Proposals.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        proposals_serializer = ProposalsSerializer(all_proposals, many=True, context={'request': self.context['request']})
        return proposals_serializer.data

    class Meta:
        model = ProposalsCategory
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    '''热搜'''
    class Meta:
        model = HotSearchWords
        fields = "__all__"