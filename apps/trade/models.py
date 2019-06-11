from datetime import datetime
from django.db import models

from goods.models import Goods

# 传统做法，从user.models中引入
# from users.models import UserProfile

# 但是当第三方模块根本不知道你的user model在哪里如何导入呢
from django.contrib.auth import get_user_model
# # 源码从setting中获取注册的自定义用户类 AUTH_USER_MODEL
User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    nums = models.IntegerField(default=0, verbose_name="购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        # 返回 商品名(购买数量)
        return f'{self.goods.name}({self.nums})'


class OrderInfo(models.Model):
    """
    订单信息: 待付款、待发货(已支付)、待收货(卖家已发货)、待评价、交易成功/失败, 待退款, 已退款、交易关闭(锁定)
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "交易完成"),
        ("REFUNDED", "已退款"),
        ("WAIT_REFUND", "待退款"),
        ("TRADE_CLOSED", "交易关闭"),
        ("WAIT_COMMENT", "待评价"),
        ("WAIT_ARRIVE", "待收货"),
        ("WAIT_SEND", "待发货"),
        ("PAY_ING", "待付款"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    # 订单号 unique 唯一
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单编号")
    # 支付宝支付时的交易号与本系统进行关联
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    # 以防用户支付到一半不支付了
    pay_status = models.CharField(choices=ORDER_STATUS, default="PAY_ING", max_length=30, verbose_name="订单状态")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户的基本信息
    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单内对应的商品
    """
    # 一个订单对应多个商品，所以添加外键
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息", related_name="order_goods")
    # 两个外键形成一张关联表
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    goods_num = models.IntegerField(default=0, verbose_name='商品数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)