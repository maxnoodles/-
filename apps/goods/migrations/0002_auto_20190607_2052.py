# Generated by Django 2.2.2 on 2019-06-07 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ['sold_num'], 'verbose_name': '商品信息', 'verbose_name_plural': '商品信息'},
        ),
    ]
