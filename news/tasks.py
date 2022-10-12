import logging
from .models import*
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .celery import app
from django.dispatch import receiver


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

@receiver(user_post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject= f'{instance.post_title}{instance.date_create.strftime("%d %m %Y")}'
        subject= f'{instance.title}! Опубликована новая запись.'
    else:
        subject = f'Appointment changer for {instance.post_title}{instance.date_create.strftime("%d %m %Y")}'
        subject = f'{instance.title} статья была изменена.'
        pass
    user_post_save.email(subject=subject, message=instance.text,)


