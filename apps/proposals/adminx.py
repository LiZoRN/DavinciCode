# Proposals/adminx.py

import xadmin
from .models import Proposals, ProposalsCategory, ProposalsImage, ProposalsCategoryBrand, Banner, HotSearchWords
from .models import IndexAd

class ProposalsAdmin(object):
    #显示的列
    list_display = ["name", "click_num", "fav_num", "total_tokens", "balance_tokens", "token_price", "token_received", "proposals_brief", "proposals_desc", "is_new", "is_hot", "create_time", "start_time", "end_time"]
    #可以搜索的字段
    search_fields = ['name', ]
    #列表页可以直接编辑的
    list_editable = ["is_hot", ]
    #过滤器
    list_filter = ["name", "click_num", "fav_num", "total_tokens", "is_new", "is_hot", "create_time", "category__name"]
    #富文本编辑器
    style_fields = {"proposals_desc": "ueditor"}

    #在添加商品的时候可以添加商品图片
    class ProposalsImagesInline(object):
        model = ProposalsImage
        exclude = ["create_time"]
        extra = 1
        style = 'tab'
    inlines = [ProposalsImagesInline]


class ProposalsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "create_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class ProposalsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]
    # 重载默认get_context方法
    def get_context(self):
        context = super(ProposalsBrandAdmin, self).get_context()
        # if 'form' in context固定写法
        if 'form' in context:
            #fields['category']，只取这个外键（分类），  category_type=1只取分类的大类
            context['form'].fields['category'].queryset = ProposalsCategory.objects.filter(category_type=1)
        return context


class BannerProposalsAdmin(object):
    list_display = ["Proposals", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "create_time"]


class IndexAdAdmin(object):
    list_display = ["category", "Proposals"]


xadmin.site.register(Proposals, ProposalsAdmin)
xadmin.site.register(ProposalsCategory, ProposalsCategoryAdmin)
xadmin.site.register(Banner, BannerProposalsAdmin)
xadmin.site.register(ProposalsCategoryBrand, ProposalsBrandAdmin)

xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)

