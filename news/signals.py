from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Post, Category
from django.contrib.auth.models import User

@receiver(post_save, sender=Post)
def send_notification_to_subscribers(sender, instance, created, **kwargs):
    if created:
        categories = instance.categories.all()
        for category in categories:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                send_mail(
                    subject=f'Новая новость в категории {category.name}',
                    message=f'Здравствуйте, {subscriber.username}\n\n'
                            f'В категории {category.name} появилась новая новость: "{instance.title}".\n',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                )


@receiver(pre_save, sender=Post)
def limit_news(sender, instance, **kwargs):
    user = instance.author
    now = timezone.now()
    post_count = Post.objects.filter(
        author=user,
        created_at__gte=now - timezone.timedelta(days=1)
    ).count()

    if post_count >= 3:
        raise   ValidationError("Вы не можете публиковать более трех новосте в сутки.")

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Добро пожаловать на наш Новостной Сайт",
            message="Большое спасибо за регистрацию. Следите за нашими обновлениями",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )