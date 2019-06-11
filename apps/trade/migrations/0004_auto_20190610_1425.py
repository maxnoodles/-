# Generated by Django 2.2.2 on 2019-06-10 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20190605_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_goods', to='trade.OrderInfo', verbose_name='订单信息'),
        ),
    ]
