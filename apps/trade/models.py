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
#     票据交易
#     """
#     ORDER_STATUS = (
#         ("TRADE_SUCCESS", "成功"),
#         ("TRADE_CLOSED", "超时关闭"),
#         ("WAIT_BUYER_PAY", "交易创建"),
#         ("TRADE_FINISHED", "交易结束"),
#         ("paying", "上链中"),
#     )
#
#     vote = models.ForeignKey(UserVotes, on_delete=models.CASCADE, verbose_name="用户")
#     tokens_trade = models.IntegerField("交易票据数", default=0)
#     transition_id = models.CharField("投票编号", max_length=30, null=True, blank=True, unique=True)
#     # 交易状态
#     trans_status = models.CharField("交易状态", choices=ORDER_STATUS, default="paying", max_length=30)
#     create_time = models.DateTimeField("添加时间", default=datetime.now)
#
#     class Meta:
#         verbose_name = "票据交易"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.transition_id)



class UserProposal(models.Model):
    """
    用户投票基本信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "上链中"),
    )

    # vote = models.ForeignKey(UserVotes, on_delete=models.CASCADE, verbose_name="用户")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案")
    token_amount = models.IntegerField("token数", default=0)
    transition_id = models.CharField("投票编号",max_length=30, null=True, blank=True, unique=True)
    # 交易状态
    trans_status = models.CharField("交易状态", choices=ORDER_STATUS, default="paying", max_length=30)

    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)


class UserProposalOption(models.Model):
    """
    用户投票详情
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "上链中"),
    )

    # vote = models.ForeignKey(UserVotes, on_delete=models.CASCADE, verbose_name="用户")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal_option = models.ForeignKey(ProposalOptions, on_delete=models.CASCADE, verbose_name="提案")
    token_amount = models.IntegerField("token数", default=0)
    transition_id = models.CharField("投票编号",max_length=30, null=True, blank=True, unique=True)
    # 交易状态
    trans_status = models.CharField("交易状态", choices=ORDER_STATUS, default="paying", max_length=30)

    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)

