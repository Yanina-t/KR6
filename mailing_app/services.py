from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
import django.utils.timezone
from django.utils import timezone

from mailing_app.models import MailingService, DeliveryLog, Message, Client


def send_mailing(mailing):
    now = timezone.localtime(timezone.now())
    log = None  # инициализируем переменную log
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
                        server_response=str(error),
                        mailing_list=mailing,
                        client=client
                    )
                    log.save()

    else:
        mailing.status = MailingService.COMPLETED
        mailing.save()
    return log


# код представляет собой функцию send_mailing, которая отвечает за отправку почтовой рассылки на основе данных из объекта MailingService.
# Внутри функции определена переменная now, которая содержит текущее локальное время.
# Затем проверяется, находится ли текущее время между временем начала и временем окончания рассылки (mailing.send_time и mailing.end_time).
# Если проверка проходит, функция перебирает все сообщения и всех клиентов, связанных с рассылкой.
# Для каждого клиента и сообщения выполняется попытка отправить почту с использованием функции send_mail.
# Если отправка проходит успешно, создается и сохраняется объект DeliveryLog с данными о попытке доставки, и функция возвращает этот объект.
# В случае ошибки (возникновения SMTPException), также создается и сохраняется DeliveryLog с информацией об ошибке.
# Если временной интервал для отправки рассылки не актуален (else), устанавливается статус рассылки в MailingService.COMPLETED,
# и функция также возвращает объект DeliveryLog, который в данном случае равен None, так как рассылка не выполняется.
# Эта функция предназначена для обработки отправки почтовых сообщений для заданной рассылки, учитывая различные условия и возможные ошибки.