# Generated by Django 2.2 on 2019-05-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190520_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='num',
            field=models.IntegerField(default=0, verbose_name='浏览量'),
        ),
    ]
