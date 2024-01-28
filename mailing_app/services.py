from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
import django.utils.timezone
from django.utils import timezone

from mailing_app.models import MailingService, DeliveryLog, Message, Client


def send_mailing(mailing):
    now = timezone.localtime(timezone.now())
    if mailing.send_time <= now <= mailing.end_time:
        for message in mailing.messages.all():
            for client in mailing.clients.all():
                try:
                    result = send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )
                    log = DeliveryLog.objects.create(
                        last_attempt_time=mailing.send_time,
                        status=result,
                        server_response='OK',
                        mailing_list=mailing,
                        client=client
                    )
                    log.save()
                    return log
                except SMTPException as error:
                    log = DeliveryLog.objects.create(
                        last_attempt_time=mailing.send_time,
                        status=False,
                        server_response=error,
                        mailing_list=mailing,
                        client=client
                    )
                    log.save()
                return log
    else:
        mailing.status = MailingService.COMPLETED
        mailing.save()
