# user_operation/serializers.py
import datetime
from rest_framework import serializers
from user_operation.models import UserFav, UserSponsorProposals, UserProposals, UserProposalOption
from rest_framework.validators import UniqueTogetherValidator
from proposals.serializers import ProposalsSerializer, ProposalsOptionsSerializer, ProposalSerializer
from .models import UserLeavingMessage,UserAddress
from proposals.models import Proposals, ProposalOptions
from proposals.serializers import ProposalsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''

    #通过提案id获取关注的天，需要嵌套提案的序列化
    proposal = ProposalsSerializer()
    class Meta:
        model = UserFav
        fields = ("proposal", "id")


class UserFavSerializer(serializers.ModelSerializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        #validate实现唯一联合，一个提案只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'proposal'),
                #message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFav
        #收藏的时候需要返回提案的id，因为取消收藏的时候必须知道提案的id是多少
        fields = ("user", "proposal",'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    用户留言
    '''
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #read_only:只返回，post时候可以不用提交，format：格式化输出
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"create_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "community", "building", "unit", "room", "create_time")

class UserSponsorProposalsDetailSerializer(serializers.ModelSerializer):
    '''
    用户发起投票详情
    '''

    #需要嵌套提案的序列化
    proposal = ProposalsSerializer()
    class Meta:
        model = UserSponsorProposals
        fields = ("proposal", "id")


class UserSponsorProposalsSerializer(serializers.ModelSerializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        #validate实现唯一联合，一个提案只能提一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserSponsorProposals.objects.all(),
                fields=('user', 'proposal'),
                #message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserSponsorProposals
        #返回提案的id
        fields = ("user", "proposal",'id')


class UserProposalDetailSerializer(serializers.ModelSerializer):
    '''
    用户参与的提案详情
    '''

    #需要嵌套提案的序列化
    proposal = ProposalsSerializer()
    class Meta:
        model = UserProposals
        fields = ("proposal", "id")


class UserProposalSerializer(serializers.ModelSerializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    def validate(self, data):
        # Apply custom validation either here, or in the view.
        if data['token_amount'] > data['proposal'].balance_tokens:
            raise serializers.ValidationError('购买票据大于可售票据数')
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        token_amount = validated_data["token_amount"]
        proposal = validated_data["proposal"]

        existed = UserProposals.objects.filter(user=user, proposal=proposal)
        if existed:
            existed = existed[0]
            existed.token_amount += token_amount
            existed.save()
            proposal = existed.proposal
            proposal.balance_tokens = proposal.balance_tokens - token_amount
            proposal.save()
        else:
            existed = UserProposals.objects.create(**validated_data)
        return existed

    class Meta:
        model = UserProposals
        fields = ("user", "proposal", "token_amount", "id")


class UserProposalOptionsDetailSerializer(serializers.ModelSerializer):
    '''
    用户提案选项详情
    '''

    #需要嵌套提案的序列化
    proposal_options = ProposalsOptionsSerializer()
    class Meta:
        model = UserProposalOption
        fields = ("proposal", "id")


class UserOptionsSerializer(serializers.ModelSerializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    def validate(self, data):
        # Apply custom validation either here, or in the view.
        token = data['token_amount']
        option = data['proposal_option']
        user = data['user']
        existed_options = ProposalOptions.objects.filter(id=option.id)
        if existed_options:
            existed_options = existed_options[0]
            existed_user_proposal = UserProposals.objects.filter(proposal=existed_options.proposals, user=user)
            if existed_user_proposal:
                if existed_user_proposal[0].token_amount < token:
                    raise serializers.ValidationError('你的票据数量不足')
        else:
            raise serializers.ValidationError('不存在该投票项')
        return data
    #继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        #获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context["request"].user
        tokes = validated_data["token_amount"]
        option = validated_data["proposal_option"]

        # 创建和修改选项票据数
        existed = UserProposalOption.objects.filter(user=user, proposal_option=option)
        if existed:
            existed = existed[0]
            existed.token_amount += tokes
            existed.save()
        else:
            existed = UserProposalOption.objects.create(**validated_data)

        # 增加选票数
        existed.proposal_option.token_received += tokes
        existed.proposal_option.proposals.token_received += tokes
        existed.proposal_option.save()
        existed.proposal_option.proposals.save()
        # 修改用户选票票据数量
        existed_user_proposal = UserProposals.objects.filter(proposal=existed.proposal_option.proposals, user=user)
        if existed_user_proposal:
            existed_user_proposal[0].token_amount -= tokes
            existed_user_proposal[0].save()
        return existed

    class Meta:
        model = UserProposalOption
        #返回提案的id
        fields = ("user", "proposal_option", "token_amount", "id")


class VoteSerializer(serializers.Serializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    token_amount = serializers.IntegerField(required=True, label="数量",min_value=1,
                                    error_messages={
                                        "min_value":"票据数量不能小于一",
                                        "required": "请选择投出票据数量"
                                    })
    #这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    #proposals是一个外键，可以通过这方法获取proposals object中所有的值
    options = serializers.PrimaryKeyRelatedField(required=True, queryset=ProposalOptions.objects.all())

    def validate(self, data):
        # Apply custom validation either here, or in the view.
        token = data['token_amount']
        option = data['options']
        user = self.context["request"].user
        existed_proposal = ProposalOptions.objects.filter(options=option)
        if existed_proposal:
            existed_proposal = existed_proposal[0]
            existed_user_proposal = UserProposals.objects.filter(proposal=existed_proposal, user=user)
            if existed_user_proposal:
                if existed_user_proposal[0].token_amount < token:
                    raise serializers.ValidationError('你的票据数量不足')
        else:
            raise serializers.ValidationError('不存在该投票项')
        data['proposal'] = existed_proposal
        data['create_time'] = datetime.now
        data['modify_time'] = datetime.now
        return data

    #继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        #获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context["request"].user
        tokes = validated_data["tokes"]
        option = validated_data["options"]

        existed = UserProposalOption.objects.filter(user=user, proposal_option=option)
        if existed:
            existed = existed[0]
            existed.token_amount += tokes
            existed.save()
        else:
            validated_data.pop['options']
            existed = UserProposalOption.objects.create(**validated_data)
        existed_user_proposal = UserProposals.objects.filter(proposal=existed.proposal, user=user)
        if existed_user_proposal:
            existed_user_proposal[0].token_amount -= tokes
        return existed
    # 不需要update接口，tokens为增投
    def update(self, instance, validated_data):
        instance.token_amount = validated_data["tokes"]
        instance.save()
        return instance
