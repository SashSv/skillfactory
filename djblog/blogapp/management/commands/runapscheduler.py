import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from blogapp.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


import datetime

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    print('hello from job')


def send_letters_to_subscribers():
    categories = Category.objects.all()
    emails = []

    for cat in categories:
        cat_subscribers = list(User.objects.filter(categories=cat))
        if cat_subscribers:
            for user in cat_subscribers:
                if user not in emails:

                    date = datetime.date.today() - datetime.timedelta(days=7)
                    posts = Post.objects.filter(created_time__gte=date)[:10]

                    html_content = render_to_string(
                        'blogapp/weekly_mail.html',
                        {
                            'posts': posts,
                            'user': user,
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject = f'Weekly mail to subscribers - Sasha blog',
                        body = '',
                        from_email='sendme.email@yandex.ru',
                        to=[user.email, ]
                    )

                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()




# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_letters_to_subscribers,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="30"
            ),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="send_letters_to_subscribers",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")