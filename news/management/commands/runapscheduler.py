import logging
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.tasks import send_weekly_newsletters

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Запуск планировщика для еженедельной рассылки"

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletters,
            trigger="interval",
            weeks=1,
            id="weekly_newsletter_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Запущена задача для рассылки писем")

        scheduler.start()

        try:
            self.stdout.write("Запуск планировщика. Нажмите Ctrl+C для остановки.\n")
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            logger.info("Остановлен планировщик")