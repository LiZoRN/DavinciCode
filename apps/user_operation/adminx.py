# user_operation/adminx.py
__author__ = 'lizorn'


import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress, UserSponsorProposals, UserProposals, UserProposalOption


class UserFavAdmin(object):
    list_display = ['user', 'proposal', "create_time"]

class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', "message", "create_time"]

class UserAddressAdmin(object):
    list_display = ["province", "city", "district", "district", "building", "unit", "room"]

class UserSponsorProposalsAdmin(object):
    list_display = ['user', 'proposal', "is_active", "create_time"]

class UserProposalsAdmin(object):
    list_display = ['user', 'proposal', "token_amount", "create_time", "modify_time"]

class UserProposalOptionAdmin(object):
    list_display = ['user', 'proposal_option', "token_amount", "create_time", "modify_time"]

xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserSponsorProposals, UserSponsorProposalsAdmin)
xadmin.site.register(UserProposals, UserProposalsAdmin)
xadmin.site.register(UserProposalOption, UserProposalOptionAdmin)