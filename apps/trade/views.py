
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permission import IsUserOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerialzer, ShopCartDetailSerializer
from .serializers import OrderInfoSerializer, OrderDetailSerializer


class ShoppingCartViewSet(ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    serializer_class = ShoppingCartSerialzer
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)
    authentication_class = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerialzer


class OrderInfoViewSet(ModelViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)
    authentication_class = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取用户购物车里的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()

        return order
