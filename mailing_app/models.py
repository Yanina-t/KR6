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


class MailingService(models.Model):
    send_time = models.DateTimeField(**NULLABLE)
    end_time = models.DateTimeField(**NULLABLE)
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=15, choices=frequency_choices, verbose_name='Frequency')
    CREATED = 'Created'
    STARTED = 'Started'
    COMPLETED = 'Completed'
    status_choices = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='created', verbose_name='Status')
    clients = models.ManyToManyField(Client, verbose_name='clients mailing_lists')

    def __str__(self):
        return f'time: {self.send_time} - {self.end_time}, periodicity: {self.frequency}, status: {self.status}'

    class Meta:
        verbose_name = 'settings mailing list'
        verbose_name_plural = 'settings mailing lists'


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    mailing_list = models.ForeignKey(MailingService, on_delete=models.CASCADE, verbose_name='рассылка',
                                     related_name='messages', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'letter'
        verbose_name_plural = 'letters'


class DeliveryLog(models.Model):
    mailing_list = models.ForeignKey(MailingService, on_delete=models.CASCADE)
    last_attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='last attempt')
    status = models.BooleanField(default=False, verbose_name='status attempt')
    server_response = models.CharField(verbose_name='server response', **NULLABLE)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='clients mailing_lists', **NULLABLE)

    def __str__(self):
        return f'{self.last_attempt_time} {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
