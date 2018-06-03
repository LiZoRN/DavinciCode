# user_operation/serializers.py

from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from proposals.serializers import ProposalsSerializer
from .models import UserLeavingMessage,UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''

    #通过提案id获取关注的天，需要嵌套提案的序列化
    proposals = ProposalsSerializer()
    class Meta:
        model = UserFav
        fields = ("proposals", "id")


class UserFavSerializer(serializers.ModelSerializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        #validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'proposals'),
                #message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFav
        #收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
        fields = ("user", "proposals",'id')


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
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "create_time", "signer_mobile")

