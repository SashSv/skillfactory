from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post, User

@receiver(post_delete, sender=Post)
def notify_managers_post_delete( sender, instance, **kwargs):
    subject = f'Пост "{instance.header} удалили с сайта."'
    mail_managers(
        subject=subject,
        message = f'Пост {instance.header}, ID - {instance.pk} удален с сайта.'
    )
    print('Done')