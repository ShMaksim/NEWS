from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext as _

@shared_task
def send_weekly_newsletters():
    now = timezone.now()
    one_week_ago = now - timedelta(weeks=1)
    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(categories=category, created_at__gte=one_week_ago)
        if posts.exists():
            for user in category.subscribers.all():
                subject = _("New articles for the week in the category %(category_name)s") % {'category_name': category.name}
                html_message = render_to_string('email/weekly_newsletter.html', {'posts': posts, 'user': user})
                plain_message = strip_tags(html_message)
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                )

@shared_task
def send_new_post_notification(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.categories.all()

    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            subject = _("New Post in Category  %(category_name)s") % {'category_name': category.name}
            html_message = render_to_string('email/new_post_notification.html', {'post': post, 'user':user})
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
