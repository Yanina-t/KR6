# Generated by Django 4.2.9 on 2024-01-28 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0011_mailinglist_end_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverylog',
            options={'verbose_name': 'log', 'verbose_name_plural': 'logs'},
        ),
        migrations.AlterModelOptions(
            name='mailinglist',
            options={'verbose_name': 'settings mailing list', 'verbose_name_plural': 'settings mailing lists'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'letter', 'verbose_name_plural': 'letters'},
        ),
        migrations.RemoveField(
            model_name='mailinglist',
            name='message',
        ),
        migrations.RemoveField(
            model_name='message',
            name='name_letter',
        ),
        migrations.AddField(
            model_name='deliverylog',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing_app.client', verbose_name='clients mailing_lists'),
        ),
        migrations.AddField(
            model_name='message',
            name='mailing_list_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letters', to='mailing_app.mailinglist', verbose_name='рассылка'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='attempt_status',
            field=models.BooleanField(verbose_name='attempt status'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='last_attempt_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='last attempt'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='server_response',
            field=models.CharField(blank=True, null=True, verbose_name='server response'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='clients',
            field=models.ManyToManyField(to='mailing_app.client', verbose_name='clients mailing_lists'),
        ),
    ]
