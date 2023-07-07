from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
# Create your models here.
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='users_mages', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:verification', kwargs={'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подверждение учетной записи для {self.user.username}'
        message = f'Перейдите по ссылке {verification_link}'
        send_mail(
            subject,
            message,
            "from@example.com",
            [self.user.email],
            fail_silently=False,
        )
