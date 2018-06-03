# trade/serializer.py
__author__ = 'lizorn'

import time

from rest_framework import serializers
from proposals.models import Proposals, ProposalOptions
from proposals.serializers import ProposalsSerializer, ProposalsOptionsSerializer
from .models import UserProposal,UserProposalOption

class UserProposalDetailSerializer(serializers.ModelSerializer):
    '''
    用户投票信息
    '''
    proposals = ProposalsSerializer(many=False, read_only=True)
    class Meta:
        model = UserProposal
        fields = ("proposals", "token_amount")


class UserProposalSerializer(serializers.Serializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    token_amount = serializers.IntegerField(required=True, label="数量",min_value=1,
                                    error_messages={
                                        "min_value":"票据数量不能小于一",
                                        "required": "请选择购买票据数"
                                    })
    #这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    #proposals是一个外键，可以通过这方法获取proposals object中所有的值
    proposals = serializers.PrimaryKeyRelatedField(required=True, queryset=Proposals.objects.all())

    #继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        #获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["token_amount"]
        proposals = validated_data["proposals"]

        existed = UserProposal.objects.filter(user=user, proposals=proposals)
        #如果购物车中有记录，数量+1
        #如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.token_amount += nums
            existed.save()
        else:
            #添加到购物车
            existed = UserProposal.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.token_amount = validated_data["token_amount"]
        instance.save()
        return instance


class UserProposalOptionDetailSerializer(serializers.ModelSerializer):
    '''
    用户投票信息
    '''
    proposal_option = ProposalsOptionsSerializer(many=False, read_only=True)
    class Meta:
        model = UserProposalOption
        fields = ("proposal_option", "token_amount")


class UserProposalOptionSerializer(serializers.Serializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    token_amount = serializers.IntegerField(required=True, label="数量",min_value=1,
                                    error_messages={
                                        "min_value":"票据数量不能小于一",
                                        "required": "请选择购买票据数"
                                    })
    #这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    #proposals是一个外键，可以通过这方法获取proposals object中所有的值
    proposal_option = serializers.PrimaryKeyRelatedField(required=True, queryset=ProposalOptions.objects.all())

    #继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        #获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["token_amount"]
        proposals = validated_data["proposal_option"]

        existed = UserProposalOption.objects.filter(user=user, proposals=proposals)
        #如果购物车中有记录，数量+1
        #如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.token_amount += nums
            existed.save()
        else:
            #添加到购物车
            existed = UserProposalOption.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.token_amount = validated_data["token_amount"]
        instance.save()
        return instance


