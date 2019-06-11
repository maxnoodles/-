import datetime
import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VerifyCode
from rest_framework.validators import UniqueValidator


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

    def validate_mobile(self, mobile):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        :param mobile: 用户注册提交到表单中的手机号码
        :return: 手机号
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是否合法
        if not re.match(self.regex_mobile, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute_ago):
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, min_length=4, max_length=4, label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 },
                                 help_text='请输入验证码')

    username = serializers.CharField(label='用户名', help_text='请输入用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])
    mobile = serializers.CharField(label='电话', max_length=11, allow_blank=True)
    password = serializers.CharField(label='密码', write_only=True, allow_blank=True, style={'input_type': 'password'})

    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 前面是将父类原有的create进行执行，后面是加入自己的逻辑
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(
            mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码已过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')

        else:
            raise serializers.ValidationError('验证码错误')

    # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
