# Generated by Django 2.2.6 on 2021-03-23 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, verbose_name='用户名')),
                ('password', models.CharField(max_length=200, verbose_name='密码')),
            ],
            options={
                'verbose_name': '测试',
            },
        ),
    ]