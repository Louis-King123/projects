# Generated by Django 2.2.6 on 2021-03-08 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='created_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='创建时间'),
        ),
    ]