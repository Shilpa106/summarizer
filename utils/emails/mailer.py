from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives


def send_email(data):
    email = EmailMultiAlternatives(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']], from_email=settings.EMAIL_HOST_USER)
    email.attach_alternative(data['attach'], "text/html")
    email.send()
