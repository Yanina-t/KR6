# Generated by Django 4.2.9 on 2024-01-28 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0012_alter_deliverylog_options_alter_mailinglist_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverylog',
            name='status_attempt',
            field=models.BooleanField(default=False, verbose_name='status attempt status'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='attempt_status',
            field=models.CharField(default='sent', max_length=20, verbose_name='attempt status'),
        ),
    ]