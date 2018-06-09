# proposals/views.py

from rest_framework.views import APIView
from proposals.serializers import ProposalsSerializer,CategorySerializer
from .models import Proposals,ProposalsCategory,Banner,HotSearchWords
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .filters import ProposalsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from .serializers import BannerSerializer,IndexCategorySerializer,HotWordsSerializer, ProposalSerializer, ProposalsOptionsSerializer
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework import permissions
from rest_framework import authentication

class ProposalsPagination(PageNumberPagination):
    '''
    投票列表自定义分页
    '''
    #默认每页显示的个数
    page_size = 12
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100


class ProposalsListViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet, mixins.CreateModelMixin):
    '''
    提案管理
    list:
        投票列表，分页，搜索，过滤，排序
    retrieve:
        获取投票详情
    create:
        创建提案
    delete:
        取消提案
    '''

    # authentication_classes = (TokenAuthentication,)
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    #这里必须要定义一个默认的排序,否则会报错
    queryset = Proposals.objects.all().order_by('id')
    # 分页
    pagination_class = ProposalsPagination
    #序列化
    serializer_class = ProposalsSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)

    # 设置filter的类为我们自定义的类
    #过滤
    filter_class = ProposalsFilter
    #搜索
    search_fields = ('name', 'brief', 'desc')
    #排序
    ordering_fields = ('total_tokens', 'token_received', 'click_num', 'fav_num')

    #投票点击数 + 1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #这里需要动态权限配置
    #1.用户注册的时候不应该有权限限制
    #2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return []
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return ProposalSerializer
        return ProposalsSerializer


class ProposalOptionViewSet(viewsets.ModelViewSet):
    '''
    提案选项管理
    list:
        投票选项列表
    retrieve:
        获取选项详情
    create:
        创建提案选项
    delete:
        删除选项
    '''
    queryset = ProposalsCategory.objects.filter(category_type=1)
    serializer_class = ProposalsOptionsSerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        投票分类列表数据(支持三级，可只使用一级别类目)
    retrieve:
        获取提案类型详情
    '''
    queryset = ProposalsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取首页轮播图：关联提案ID
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页
    """
    # 获取is_tab=True（导航栏）里面的分类下的投票数据
    queryset = ProposalsCategory.objects.filter(is_tab=True, name__in=["物业", "业务会"])
    serializer_class = IndexCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    热搜
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer