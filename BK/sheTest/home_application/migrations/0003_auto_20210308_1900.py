# Generated by Django 2.2.6 on 2021-03-08 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_history_created_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='request_id',
        ),
        migrations.AlterField(
            model_name='history',
            name='inst_finish',
            field=models.BooleanField(default=False, verbose_name='是否完成'),
        ),
        migrations.AlterField(
            model_name='history',
            name='inst_id',
            field=models.IntegerField(max_length=128, verbose_name='作业ID'),
        ),
        migrations.AlterField(
            model_name='history',
            name='inst_status',
            field=models.BooleanField(default=False, verbose_name='作业状态'),
        ),
    ]
