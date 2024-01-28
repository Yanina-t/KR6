from mailing_app.services import send_mailing
from mailing_app.models import MailingList


def daily_tasks():
    mailings = MailingList.objects.filter(periodicity="Daily", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = MailingList.objects.filter(periodicity="Weekly", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = MailingList.objects.filter(periodicity="Monthly", status="Started")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)
