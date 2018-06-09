#proposals/models.py
__author__ = 'lizorn'


from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField


class ProposalsCategory(models.Model):
    """
    提案分类
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField('类别名',default="", max_length=30,help_text="类别名")
    code = models.CharField("类别code",default="", max_length=30,help_text="类别code")
    desc = models.TextField("类别描述",default="",help_text="类别描述")
    #目录树级别
    category_type = models.IntegerField("类目级别",choices=CATEGORY_TYPE,help_text="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat")
    is_tab = models.BooleanField("是否导航",default=False,help_text="是否导航")
    create_time = models.DateTimeField("添加时间",default=datetime.now, help_text="创建时间")

    class Meta:
        verbose_name = "提案类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Proposals(models.Model):
    """
    提议
    """
    category = models.ForeignKey(ProposalsCategory, on_delete=models.CASCADE, verbose_name="提案类型", help_text="提案类别")
    proposal_sn = models.CharField("提案唯一编码（标准待定）",max_length=50, default="",help_text="提案编码")
    name = models.CharField("提案名",max_length=100,help_text="标题")
    click_num = models.IntegerField("点击数",default=0,help_text="点击数量")
    fav_num = models.IntegerField("收藏数", default=0,help_text="关注数")
    brief = models.TextField("投票简短描述", max_length=500,default='',help_text="简述")
    desc = UEditorField(verbose_name=u"内容", imagePath="proposals/images/", width=1000, height=300,
                              filePath="proposals/files/", default='',help_text="内容详情")
    total_tokens = models.IntegerField("总票据数(B)", default=0, help_text="总票据数")
    balance_tokens = models.IntegerField("可售票据数(B)", default=0, help_text="可售票据数")
    token_price = models.IntegerField("票据价格(B)", default=0, help_text="票据价格")
    token_received = models.IntegerField("收到总投票数", default=0, help_text="收到总票数")

    # 首页中展示的提案封面图
    proposal_front_image = models.ImageField(upload_to="proposals/images/", null=True, blank=True, verbose_name="封面图",help_text="封面")
    is_new = models.BooleanField("是否新发起",default=False, help_text="是否新发起")
    is_hot = models.BooleanField("是否高关注",default=False,help_text='是否高关注')
    is_anonymous = models.BooleanField("是否匿名", default=False, help_text='是否匿名')
    is_blockchain = models.BooleanField("是否启用区块链", default=False, help_text='是否启用区块链')
    start_time = models.DateTimeField("开始时间",default=datetime.now, help_text='发起时间')
    end_time = models.DateTimeField("结束时间", default=datetime.now, help_text='结束时间')
    create_time = models.DateTimeField("添加时间",default=datetime.now, help_text='创建时间')

    class Meta:
        verbose_name = '提案信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProposalsImage(models.Model):
    """
    提案详情轮播图
    """
    proposals = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    create_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '投票轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.proposals.name

class ProposalOptions(models.Model):
    """
    提案选项
    """
    proposals = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="投票选项", related_name="options")
    name = models.CharField("选项", max_length=50, default="")
    desc = models.TextField("选项描述", default="", max_length=200, help_text="选项描述")
    token_received = models.IntegerField("票数", default=0)
    images = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    create_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '投票选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.proposals.name, self.name)



class Banner(models.Model):
    """
    首页轮播
    """
    proposals = models.ForeignKey(Proposals, on_delete=models.CASCADE, verbose_name="提案",help_text='提案')
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片",help_text='图片')
    index = models.IntegerField("轮播顺序",default=0, help_text='轮播顺序')
    create_time = models.DateTimeField("添加时间", default=datetime.now,help_text='创建时间')

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.proposals.name


class IndexAd(models.Model):
    """
    提案广告
    """
    category = models.ForeignKey(ProposalsCategory, on_delete=models.CASCADE, related_name='category',verbose_name="提案类型")
    proposals =models.ForeignKey(Proposals, on_delete=models.CASCADE, related_name='proposals')

    class Meta:
        verbose_name = '提案广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.proposals.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField("热搜词",default="", max_length=20)
    index = models.IntegerField("排序",default=0)
    create_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '热搜排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords


class ProposalsCategoryBrand(models.Model):
    """
    提案方
    """
    category = models.ForeignKey(ProposalsCategory, on_delete=models.CASCADE, related_name='brands', null=True, blank=True, verbose_name="投票类目")
    name = models.CharField("提案品牌名",default="", max_length=30,help_text="品牌名")
    desc = models.TextField("品牌描述",default="", max_length=200,help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    create_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "提案品牌"
        verbose_name_plural = verbose_name
        db_table = "proposals_proposalsbrand"

    def __str__(self):
        return self.name
