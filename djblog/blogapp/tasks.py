from celery import shared_task
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime


# Функция для рассылки при создании новости
@shared_task
def new_post_notification(post_id):

    new_post = Post.objects.get(pk=post_id)
    categories = Category.objects.filter(posts=new_post)
    subscribers_email_list = []

    for cat in categories:
        cat_subscribers = list(User.objects.filter(categories=cat))
        subscribers_email_list += cat_subscribers

    for user in set(subscribers_email_list):
        html_content = render_to_string(
            'blogapp/new_post_mail.html',
            {
                'new_post': new_post,
                'user': user,
                'site_domain': 'http://127.0.0.1:8000',  # подставляем адрес домена автоматом в письмо
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{new_post.header[:20]} - Sasha blog',
            body='',
            from_email='sendme.email@yandex.ru',
            to=[user.email, ]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# Функция для рассылки подборок всем подписчикам
@shared_task
def send_letters_to_all_subscribers():
    print('start task')
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