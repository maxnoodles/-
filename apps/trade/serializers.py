import time
import random

from rest_framework import serializers
from .models import ShoppingCart, OrderGoods, OrderInfo
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 一条购物车关系记录对应的只有一个goods。
    goods = GoodsSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


class ShoppingCartSerialzer(serializers.Serializer):
    # 使用Serializer本身最好, 因为它是灵活性最高的。
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label='数量', min_value=1,
                                    error_messages={
                                        'min_value': '商品数量不能小于一',
                                        'required': '请选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Goods.objects.all()
    )

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    order_mount = serializers.FloatField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    def get_total_price(self):
        """计算订单金额"""
        goods = ShoppingCart.objects.filter(user=self.context['request'].user)
        total_price = 0.0
        for good in goods:
            total_price += (good.nums * good.goods.shop_price)
        return total_price

    def generate_order_sn(self):
        """生成随机订单号"""
        time_str = time.strftime('%Y%m%d%H%M%S')
        user_id = self.context['request'].user.id
        rand_str = random.randint(10, 99)
        order_sn = f'{time_str}{user_id}{rand_str}'
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        attrs['order_mount'] = self.get_total_price()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 一个订单有多个订单商品项
    order_goods = OrderGoodsSerialzier(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"
