from rest_framework import generics, mixins
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, GoodsCategorySerializer
from .filters import GoodsFilter
# from rest_framework.authentication import TokenAuthentication


# 商品列表分页类
class GoodsPagination(PageNumberPagination):
    page_size = 8
    # 向后台要多少条
    page_size_query_param = 'page_size'
    # 定制多少页的参数
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序,取某一个具体商品的详情
    """
    queryset = Goods.objects.all()
    # authentication_classes = (TokenAuthentication, )
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 设置我们的search字段
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 设置排序
    ordering_fields = ('sold_num', 'add_time')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


