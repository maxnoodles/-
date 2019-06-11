from django.shortcuts import render
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer
from .serializers import LeavingMessageSerializer, UserAddressSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permission import IsUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


class UserFavViewSet(ModelViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    # 权限
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)
    # 认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # url 详情页后缀
    lookup_field = 'goods_id'

    # 获取用户自己的UserFav
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 动态获取serializers
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavDetailSerializer


class UserLeavingMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
     list:
         获取用户留言
     create:
         添加留言
     delete:
         删除留言功能
     """
    serializer_class = LeavingMessageSerializer

    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressSerializerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
     收货地址管理
     list:
         获取收货地址
     create:
         添加收货地址
     update:
         更新收货地址
     delete:
         删除收货地址
     """
    serializer_class = UserAddressSerializer

    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
