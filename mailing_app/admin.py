from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, MailingService, DeliveryLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'full_name', 'user_client')


@admin.register(MailingService)
class MailingServiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'send_time', 'frequency', 'status', 'user_mailing')


@admin.register(DeliveryLog)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing_list', 'last_attempt_time', 'status',)
