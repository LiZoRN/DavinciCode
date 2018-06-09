"""DavinciCode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
import xadmin
from django.views.static import serve
from DavinciCode.settings import MEDIA_ROOT

from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from proposals.views import ProposalsListViewSet, CategoryViewSet, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset, \
        UserSponsorProposalsViewset, UserOptionsViewset, UserProposalViewset, VoteViewset

router = DefaultRouter()

# 配置goods的url
router.register(r'proposals', ProposalsListViewSet, base_name='proposals')
# 配置Category的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
# 配置codes的url
router.register(r'sms', SmsCodeViewset, base_name="code")
# 配置用户的url
router.register(r'users', UserViewset, base_name="users")
# 配置收货地址
router.register(r'address', AddressViewset, base_name="address")
# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")
# 配置用户投票发起url
router.register(r'sponsor', UserSponsorProposalsViewset, base_name="sponsor")
# 配置用户购买票据url
router.register(r'buytokes', UserProposalViewset, base_name="buytokes")
# 配置用户投票url
router.register(r'vote', UserOptionsViewset, base_name="vote")
# 配置用户投票url
# router.register(r'vote2', VoteViewset, base_name="vote2")


# 配置首页轮播图的url
router.register(r'banners', BannerViewset, base_name="banners")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # api列表页
    path('api/', include(router.urls)),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    path('login/', obtain_jwt_token),
    # drf文档，title自定义
    path('docs', include_docs_urls(title='投票系统')),
    # 首页
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
