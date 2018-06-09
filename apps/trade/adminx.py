# trade/adminx.py
__author__ = 'lizorn'

import xadmin
from .models import OrderInfo, OrderProposalTokens, OrderOptionsTokens


class OrderInfoAdmin(object):
    list_display = ["user", "proposals", "token_nums", ]
    # class TokensTradeInline(object):
    #     model = TokensTrade
    #     exclude = ['create_time', ]
    #     extra = 1
    #     style = 'tab'

    class UserProposalInline(object):
        model = OrderProposalTokens
        exclude = ['create_time', ]
        extra = 1
        style = 'tab'

    class UserProposalOptionInline(object):
        model = OrderOptionsTokens
        exclude = ['create_time', ]
        extra = 1
        style = 'tab'

    inlines = [UserProposalInline, UserProposalOptionInline,]


xadmin.site.register(OrderInfo, OrderInfoAdmin)
