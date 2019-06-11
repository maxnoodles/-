import random

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.alidayu import DaYu
from .models import VerifyCode
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, request, username=None, password=None):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    """
    发送验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位验证码
        """
        seeds = '1234567890'
        code = ''.join([random.choice(seeds) for i in range(0, 4)])
        return code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        dayu = DaYu()
        sms_status = dayu.send_msg(mobile=mobile, code=code)

        if sms_status['Code'] == 'OK':
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({'mobile': sms_status['Message']},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mobile': mobile},
                            status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    用户操作
    """
    queryset = User.objects.all()
    # 认证方式
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 动态序列化
    def get_serializer_class(self):
        if self.action == 'retrieve':
            # IsAuthenticated() 拒绝允许任何未认证用户
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        else:
            return UserDetailSerializer

    # 动态选择验证
    def get_permissions(self):
        if self.action == 'retrieve':
            # IsAuthenticated() 拒绝允许任何未认证用户
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        else:
            return []

    # 重写create方法，添加额外信息token, name
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法，不管传什么id，都只返回当前状态
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
