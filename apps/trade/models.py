# trade/models.py
__author__ = 'lizorn'

from datetime import datetime
from django.db import models

from proposals.models import Proposals, ProposalOptions

# get_user_model方法会去setting中找AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
#
# class TokensTrade(models.Model):
#     """
#     区块交易信息
#     """
#     ORDER_STATUS = (
#         ("TRADE_SUCCESS", "成功"),
#         ("TRADE_CLOSED", "超时关闭"),
#         ("WAIT_BUYER_PAY", "交易创建"),
#         ("TRADE_FINISHED", "交易结束"),
#         ("paying", "上链中"),
#     )
#
#     transition_id = models.CharField("投票编号", max_length=30, null=True, blank=True, unique=True)
#     trans_status = models.CharField("交易状态", choices=ORDER_STATUS, default="paying", max_length=30)
#     sender = models.CharField("")
#     create_time = models.DateTimeField("添加时间", default=datetime.now)
#
#     class Meta:
#         verbose_name = "区块交易信息"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.transition_id)
#
class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )
    PAY_TYPE = (
        # ("alipay", "支付宝"),
        # ("wechat", "微信"),
        ("antb","antB"),
    )
    # vote = models.ForeignKey(UserVotes, on_delete=models.CASCADE, verbose_name="用户")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    # 订单号唯一
    order_sn = models.CharField("订单编号", max_length=30, null=True, blank=True, unique=True)
    transition_id = models.CharField("投票编号",max_length=30, null=True, blank=True, unique=True)
    # 交易状态
    trans_status = models.CharField("交易状态", choices=ORDER_STATUS, default="paying", max_length=30)
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)


class OrderProposalTokens(models.Model):
    """
    用户票据购买信息
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案")
    token_amount = models.IntegerField("token数", default=0)
    transition_id = models.CharField("交易编号",max_length=30, null=True, blank=True, unique=True)
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)

class OrderOptionsTokens(models.Model):
    """
    用户投票tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal_option = models.ForeignKey(ProposalOptions, on_delete=models.CASCADE, verbose_name="提案")
    transition_id = models.CharField("交易编号", max_length=30, null=True, blank=True, unique=True)
    token_amount = models.IntegerField("token数", default=0)
    sender_to = models.IntegerField("接收者", default=0)
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)