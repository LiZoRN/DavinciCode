# trade/adminx.py
__author__ = 'lizorn'

import xadmin
from .models import UserProposal, UserProposalOption


class UserProposalAdmin(object):
    list_display = ["user", "proposals", "token_nums", ]
    # class TokensTradeInline(object):
    #     model = TokensTrade
    #     exclude = ['create_time', ]
    #     extra = 1
    #     style = 'tab'

    class UserProposalOptionInline(object):
        model = UserProposalOption
        exclude = ['create_time', ]
        extra = 1
        style = 'tab'

    inlines = [UserProposalOption, ]


xadmin.site.register(UserProposal, UserProposalAdmin)
