from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_event_created_email(user_email, event_name):
    subject = 'New Event Created'
    message = f'You have successfully created a new event: "{event_name}".'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_event_approved_email(user_email, event_name):
    subject = 'Event Approved'
    message = f'Your event have successfully approved: "{event_name}".'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_event_delete_email(user_email, event_name):
    subject = 'Event Deleted'
    message = f'Your event have successfully deleted: "{event_name}".'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)