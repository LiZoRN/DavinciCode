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
from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from DavinciCode.settings import MEDIA_ROOT

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from proposals.views import ProposalsListViewSet,CategoryViewSet,BannerViewset,IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()

#配置goods的url
router.register(r'proposals', ProposalsListViewSet,base_name='goods')
# 配置Category的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")
#配置用户的url
router.register(r'users', UserViewset, base_name="users")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # api列表页
    path('api/', include(router.urls)),
    # drf文档，title自定义
    path('docs', include_docs_urls(title='投票系统')),
    # 首页
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
