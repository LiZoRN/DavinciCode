# user_operation/models.py
__author__ = 'lizorn'


from datetime import datetime
from django.db import models
from proposals.models import Proposals, ProposalOptions

from django.contrib.auth import get_user_model
User = get_user_model()

class UserFav(models.Model):
    """
    用户关注
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案", help_text="提案id")
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = '用户关注'
        verbose_name_plural = verbose_name
        unique_together = ("user", "proposal")

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    """
    用户住址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户" )
    code = models.CharField("小区", max_length=100, default="", blank=True)
    province = models.CharField("省份",max_length=100, default="", help_text="省")
    city = models.CharField("城市",max_length=100, default="", help_text="市")
    district = models.CharField("区域",max_length=100, default="", help_text="区")
    community = models.CharField("小区",max_length=100, default="", help_text="社区")
    building = models.CharField("幢", max_length=100, default="", help_text="幢")
    unit = models.CharField("单元", max_length=100, default="", help_text="单元")
    room = models.CharField("室", max_length=100, default="", help_text="室")
    address = models.CharField("详细地址",max_length=100, default="",help_text="详细地址")
    create_time = models.DateTimeField("添加时间",default=datetime.now)
    modify_time = models.DateTimeField("修改时间",default=datetime.now)

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                      help_text=u"留言类型: 1(留言),2(投诉),3(询问)")
    subject = models.CharField("主题",max_length=100, default="", help_text="标题")
    message = models.TextField("留言内容",default="",help_text="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", blank=True, help_text="上传的文件")
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserSponsorProposals(models.Model):
    """
    用户发起提案
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案", help_text="提案id")
    is_active = models.BooleanField("是否有效", default=True, help_text='是否有效')
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = '用户发起投票'
        verbose_name_plural = verbose_name
        unique_together = ("user", "proposal")

    def __str__(self):
        return self.user.username


class UserProposals(models.Model):
    """
    用户参与的提案信息
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案", help_text="提案id")
    token_amount = models.IntegerField("token数", default=0, help_text="票据数量（投票权重）")
    create_time = models.DateTimeField("添加时间",default=datetime.now)
    modify_time = models.DateTimeField("修改时间",default=datetime.now)

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)


class UserProposalOption(models.Model):
    """
    用户投票详情
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    proposal_option = models.ForeignKey(ProposalOptions, on_delete=models.CASCADE, verbose_name="投票选项")
    token_amount = models.IntegerField("token数", default=0)
    create_time = models.DateTimeField("添加时间",default=datetime.now)
    modify_time = models.DateTimeField("修改时间", default=datetime.now)

    class Meta:
        verbose_name = "用户投票详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.transition_id)


