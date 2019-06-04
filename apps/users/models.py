from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户表
    """
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=(('male', "男"), ('female', '女')),
                              default='female', verbose_name='性别')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='邮箱')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
