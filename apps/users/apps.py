from django.apps import AppConfig
from django.contrib.auth import get_user_model


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户'

    def ready(self):
        import users.signals