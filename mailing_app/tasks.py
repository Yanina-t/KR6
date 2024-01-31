from mailing_app.services import send_mailing
from mailing_app.models import MailingService


def daily_tasks():
    mailings = MailingService.objects.filter(frequency="Daily", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = MailingService.objects.filter(frequency="Weekly", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = MailingService.objects.filter(frequency="Monthly", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)

# Функция daily_tasks извлекает все экземпляры модели MailingService,
# у которых установлено значение частоты "Daily" и статус "Started", используя метод filter из ORM Django.
# Затем проверяется, существуют ли такие рассылки, используя метод exists.
