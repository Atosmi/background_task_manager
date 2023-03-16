from celery import shared_task 

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from time import sleep

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_email_task():
    usuarios = get_user_model().objects.all()
    for user in usuarios:
        sleep(2)
        send_mail('Heyy Celery task worked!',
        'This is proof the task worked!',
        '--------------------------------',
        [user.email])

    return None
