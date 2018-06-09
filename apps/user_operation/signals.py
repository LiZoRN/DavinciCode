# users_operation/signals.py

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from user_operation.models import UserFav,UserProposals, UserProposalOption

# post_save:接收信号的方式
#sender: 接收信号的model
@receiver(post_save, sender=UserFav)
def create_UserFav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    if created:
        proposal = instance.proposal
        proposal.fav_num += 1
        proposal.save()

@receiver(post_delete, sender=UserFav)
def delete_UserFav(sender, instance=None, created=False, **kwargs):
        proposal = instance.proposal
        proposal.fav_num -= 1
        proposal.save()


#sender: 接收信号的model
@receiver(post_save, sender=UserProposals)
def create_UserProposals(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    if created:
        proposal = instance.proposal
        proposal.balance_tokens = proposal.balance_tokens - instance.token_amount
        proposal.save()

@receiver(post_delete, sender=UserProposals)
def delete_UserProposals(sender, instance=None, created=False, **kwargs):
    proposal = instance.proposal
    proposal.balance_tokens = proposal.balance_tokens + instance.token_amount
    proposal.save()

# @receiver(post_save, sender=UserProposals)
# def delete_UserProposalOption(sender, instance=None, created=False, **kwargs):
#     proposal = instance.proposal_option.proposal
#     user = instance.user
#     existed_user_proposal = UserProposals.objects.filter(proposal=proposal, user=user)
#     if existed_user_proposal:
#         proposal.balance_tokens = proposal.balance_tokens + instance.token_amount
#         proposal.save()

#sender: 接收信号的model
@receiver(post_delete, sender=UserProposalOption)
def delete_UserProposalOption(sender, instance=None, created=False, **kwargs):
    # 增加选票数
    instance.proposal_option.proposals.token_received -= instance.token_amount
    instance.proposal_option.token_received -= instance.token_amount
    instance.proposal_option.save()
    instance.proposal_option.proposals.save()
    # 修改用户选票票据数量
    existed_user_proposal = UserProposals.objects.filter(proposal=instance.proposal_option.proposals, user=instance.user)
    if existed_user_proposal:
        existed_user_proposal[0].token_amount += instance.token_amount
        existed_user_proposal[0].save()