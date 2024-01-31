# Generated by Django 5.0.1 on 2024-01-27 16:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0009_rename_name_latter_message_name_letter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverylog',
            name='attempt_time',
        ),
        migrations.RemoveField(
            model_name='deliverylog',
            name='status',
        ),
        migrations.AddField(
            model_name='deliverylog',
            name='attempt_status',
            field=models.CharField(choices=[('sent', 'The message was sent successful'), ('failed', 'Error sending email'), ('delivered', 'The message was successfully delivered to the recipient'), ('deferred', 'Delivery has been delayed, possibly due to technical reasons.'), ('bounced', 'The email could not be delivered and was rejected by the recipients server.')], default='sent', max_length=20, verbose_name='attempt status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliverylog',
            name='last_attempt_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last attempt'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='server_response',
            field=models.TextField(verbose_name='server response'),
        ),
    ]
