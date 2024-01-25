from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')
    full_name = models.CharField(max_length=100, verbose_name='Full name')
    comment = models.TextField(blank=True, verbose_name='Comment')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.email}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class MailingList(models.Model):
    send_time = models.DateTimeField()
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=15, choices=frequency_choices, verbose_name='Frequency')
    status_choices = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='created', verbose_name='Status')


class Message(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()


class DeliveryLog(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)
    server_response = models.TextField()

    def __str__(self):
        return f"{self.message.mailing_list} - {self.status}"