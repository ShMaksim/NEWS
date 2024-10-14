from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Post, Category
from django.contrib.auth.models import User
from .tasks import send_new_post_notification
from django.core.cache import cache
from django.utils.translation import gettext as _


@receiver(post_save, sender=Post)
def send_notification_to_subscribers(sender, instance, created, **kwargs):
    if created:
        send_new_post_notification.delay(instance.id)


@receiver(pre_save, sender=Post)
def limit_news(sender, instance, **kwargs):
    user = instance.author
    now = timezone.now()
    post_count = Post.objects.filter(
        author=user,
        created_at__gte=now - timezone.timedelta(days=1)
    ).count()

    if post_count >= 3:
        raise   ValidationError(_("You can't post more than three stories per day."))

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=_("Welcome to our News Site"),
            message=_("Thank you very much for registering. Stay tuned"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )

@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, **kwargs):
    cache_key = f'post_{instance.pk}'
    cache.delete(cache_key)

@receiver(post_delete, sender=Post)
def post_delete_handler(sender, instance, **kwargs):
    cache_key = f'post_{instance.pk}'
    cache.delete(cache_key)