from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=User)
def create_user(sender, **kwargs):
    if kwargs['created']:
        password = kwargs['instance'].password
        kwargs['instance'].set_password(password)
        kwargs['instance'].save()
