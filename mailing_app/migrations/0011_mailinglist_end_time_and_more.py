# Generated by Django 4.2.9 on 2024-01-27 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0010_remove_deliverylog_attempt_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='server_response',
            field=models.TextField(blank=True, null=True, verbose_name='server response'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
