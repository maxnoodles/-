from .models import Goods, GoodsCategory, GoodsImage
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


class GoodsSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ('id', 'name', 'goods_sn', 'goods_front_image')

