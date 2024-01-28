from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, MailingList, Message, DeliveryLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('send_time', 'frequency', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(DeliveryLog)
class LogAdmin(admin.ModelAdmin):
    list_display = ('mailing_list', 'last_attempt_time', 'attempt_status')
