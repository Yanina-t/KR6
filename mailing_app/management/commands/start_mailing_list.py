import logging

logging.basicConfig(level=logging.INFO)

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing_app.tasks import daily_tasks, weekly_tasks, monthly_tasks

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """ Функция используется для удаления старых выполненных задач.
    Декоратор @util.close_old_connections используется для автоматического закрытия старых баз данных перед выполнением функции."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_tasks,
            trigger=CronTrigger(minute="*/1"),
            id="daily_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'daily_job'.")

        scheduler.add_job(
            weekly_tasks,
            trigger=CronTrigger(day_of_week="*/1"),
            id="weekly_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_job'.")

        scheduler.add_job(
            monthly_tasks,
            trigger=CronTrigger(day="*/30"),
            id="monthly_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'monthly_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
            self.stdout.write(self.style.SUCCESS('Successfully ran your custom command'))
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))

# В целом, этот код создает и конфигурирует планировщик задач APScheduler, добавляет различные задачи,
# такие как ежедневные, еженедельные, ежемесячные задачи, а также задачу для удаления старых выполненных задач.
# Затем он запускает планировщик, который будет выполнять эти задачи в фоновом режиме в соответствии с заданными временными интервалами.
# logging используется для ведения логов.
# settings содержит настройки Django.
# BlockingScheduler из apscheduler.schedulers.blocking - это тип планировщика, который будет блокировать выполнение кода,
# чтобы обеспечить стабильную работу планирования.
# CronTrigger из apscheduler.triggers.cron - это триггер, который позволяет настраивать выполнение задач по расписанию в формате cron.
# BaseCommand из django.core.management.base - базовый класс для создания собственных команд управления Django.
# DjangoJobStore, DjangoJobExecution и util - компоненты, предоставляемые django_apscheduler для интеграции APScheduler с Django.
# daily_tasks, weekly_tasks, monthly_tasks - функции, представляющие собой задачи, которые вы хотите выполнять с использованием планировщика.
