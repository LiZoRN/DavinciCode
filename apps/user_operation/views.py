# user_operaton/views.py

from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav,UserLeavingMessage,UserAddress,UserSponsorProposals,UserProposals,UserProposalOption
from proposals.models import Proposals
from proposals.serializers import ProposalsSerializer
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer,AddressSerializer,\
    UserProposalSerializer , UserOptionsSerializer, UserSponsorProposalsDetailSerializer, UserSponsorProposalsSerializer, VoteSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    '''
    list:
        获取关注列表
    create:
        添加关注
    delete:
        取消关注
    retrieve:
        获取关注详情
    '''
    #permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    #auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    #搜索的字段
    lookup_field = 'proposal_id'

    #动态选择serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        elif self.action == "retrieve":
            return UserFavDetailSerializer
        return UserFavSerializer

    def get_queryset(self):
        #只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    #用信号量实现了
    #  用户收藏的商品数量+1
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     # 这里instance相当于UserFav model，通过它找到proposals
    #     proposals = instance.proposals
    #     proposals.fav_num += 1
    #     proposals.save()


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    # 只能看到自己的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    用户住址管理
    list:
        获取用户地址
    create:
        添加住址
    update:
        更新地址
    delete:
        删除地址
    retrieve:
        获取住址详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

class UserSponsorProposalsViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    '''
    list:
        获取用户发起的投票列表
    create:
        发起投票
    delete:
        取消关联
    retrieve:
        获取投票详情
    '''
    #permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    #auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    #搜索的字段
    lookup_field = 'proposal_id'

    #动态选择serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserSponsorProposalsDetailSerializer
        elif self.action == "create":
            return UserSponsorProposalsDetailSerializer
        return UserSponsorProposalsSerializer

    def get_queryset(self):
        #只能查看当前登录用户的发起的投票，不会获取所有用户发起的投票
        return UserSponsorProposals.objects.filter(user=self.request.user)

class UserProposalViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    用户票据管理
    list:
        获取用户antb票据情况
    create:
        用户购买投票票据（区块链）
    retrieve:
        获取用户票据详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserProposalSerializer

    def get_queryset(self):
        return UserProposals.objects.filter(user=self.request.user)

class UserOptionsViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,  mixins.RetrieveModelMixin, mixins.DestroyModelMixin, ):
    """
    投票管理
    list:
        获取个人投票列表
    create：
        投票
    retrieve:
        查看投票详情
    delete:
        删除选项（antb支付情况下不支持）
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserOptionsSerializer

    def get_queryset(self):
        return UserProposalOption.objects.filter(user=self.request.user)

class VoteViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
    投票管理
    list:
        获取个人投票列表
    create：
        投票
    retrieve:
        查看投票详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = VoteSerializer
    #options的id
    lookup_field = "proposal_option_id"

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return UserSponsorProposalsSerializer
    #     else:
    #         return VoteSerializer

    #获取投票列表
    def get_queryset(self):
        return UserProposalOption.objects.filter(user=self.request.user)