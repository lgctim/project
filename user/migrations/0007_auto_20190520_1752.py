# Generated by Django 2.2 on 2019-05-20 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190517_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='标签')),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='md',
        ),
        migrations.RemoveField(
            model_name='book',
            name='nb',
        ),
        migrations.AddField(
            model_name='book',
            name='good',
            field=models.CharField(choices=[('诺贝尔文学奖', '诺贝尔文学奖'), ('茅盾文学奖', '茅盾文学奖')], default=None, max_length=32, verbose_name='获奖'),
        ),
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Tags', verbose_name='标签'),
        ),
    ]
