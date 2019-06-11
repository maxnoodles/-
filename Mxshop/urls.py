"""Mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
import xadmin
from django.views.static import serve
from Mxshop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from users.views import SmsCodeViewSet, UserViewSet
from rest_framework.documentation import include_docs_urls
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressSerializerViewSet
from trade.views import ShoppingCartViewSet, OrderInfoViewSet

router = DefaultRouter()

"""接口1: 商品接口"""
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置Category的api
router.register(r'category', CategoryViewSet, base_name='category')
# 配置请求验证码的api
router.register(r'code', SmsCodeViewSet, base_name="code")
# 配置登录的api
router.register(r'user', UserViewSet, base_name='user')
# 配置用户收藏api
router.register(r'user_fav', UserFavViewSet, base_name='user_fav')
# 配置用户留言api
router.register(r'user_msg', UserLeavingMessageViewSet, base_name='user_msg')
# 配置用户地址api
router.register(r'user_add', UserAddressSerializerViewSet, base_name='user_add')
# 配置购物车api
router.register(r'shop_cart', ShoppingCartViewSet, base_name='shop_cart')
# 配置订单api
router.register(r'order', OrderInfoViewSet, base_name='order')

urlpatterns = [
    path('', include(router.urls)),
    path('xadmin/', xadmin.site.urls),
    path('api_auth/', include('rest_framework.urls'), name='rest_framework'),
    path('jwt_token_auth/', obtain_jwt_token),
    path('doc/', include_docs_urls(title='慕学生鲜')),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
]
