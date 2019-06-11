from datetime import datetime
from django.db import models

from goods.models import Goods
# 但是当第三方模块根本不知道你的user model在哪里如何导入呢
from django.contrib.auth import get_user_model
# # 源码从setting中获取注册的自定义用户类 AUTH_USER_MODEL
User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

        # 多个字段作为一个联合唯一索引
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    province = models.CharField(max_length=100, default="", verbose_name="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_type = models.IntegerField(choices=MESSAGE_CHOICES, default=1, verbose_name='留言类型',
                                       help_text='留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)')
    subject = models.CharField(max_length=100, default='', verbose_name='主题')
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
