# trade/serializer.py
__author__ = 'lizorn'

import time

from rest_framework import serializers
from proposals.models import Proposals, ProposalOptions
from proposals.serializers import ProposalsSerializer, ProposalsOptionsSerializer
from .models import OrderInfo,OrderProposalTokens,OrderOptionsTokens

class OrderProposalsTokensDetailSerializer(serializers.ModelSerializer):
    '''
    用户投票信息
    '''
    proposal = ProposalsSerializer(many=False, read_only=True)
    class Meta:
        model = OrderOptionsTokens
        fields = ("proposal", "token_amount")

class OrderOptionsTokensDetailSerializer(serializers.ModelSerializer):
    '''
    用户投票信息
    '''
    options = ProposalsOptionsSerializer(many=False, read_only=True)
    class Meta:
        model = OrderOptionsTokens
        fields = ("options", "token_amount")

class OrderProposalSerializer(serializers.Serializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 生成订单的时候这些不用post
    # pay_status = serializers.CharField(read_only=True)
    # trade_no = serializers.CharField(read_only=True)
    # order_sn = serializers.CharField(read_only=True)
    # pay_time = serializers.DateTimeField(read_only=True)
    # nonce_str = serializers.CharField(read_only=True)
    # pay_type = serializers.CharField(read_only=True)

    def get_alipay_url(self, obj):

        pass

    def generate_order_sn(self):
        # 生成订单号
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn，然后在view中就可以save
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"

