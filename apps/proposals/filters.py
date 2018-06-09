# proposals/filters.py

import django_filters

from .models import Proposals
from django.db.models import Q

class ProposalsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品过滤的类
    '''
    #两个参数，name是要过滤的字段，lookup是执行的行为，‘小与等于本店价格’
    token_rcv_min = django_filters.NumberFilter(name="token_received", lookup_expr='gte',help_text='最小价格')
    token_rcv_max = django_filters.NumberFilter(name="token_received", lookup_expr='lte',help_text='最小大价格')
    top_category = django_filters.NumberFilter(name="category", method='top_category_filter',help_text='类别')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级分类二级分类还是三级分类，都能找到。
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Proposals
        fields = ['token_price','is_hot','is_new']

