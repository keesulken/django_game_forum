import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from .models import *


@shared_task
def weekly_mailing(sender, **kwargs):
    for post in Post.objects.filter(publishing_date__gt=(datetime.date.today() - datetime.timedelta(days=7))):
        for cat in PostCategory.objects.filter(post=post):
            for subscriber in Subscribers.objects.filter(category=cat.categories):
                msg = EmailMultiAlternatives(
                    subject=post.title,
                    body=post.content,
                    from_email='yv9v@yandex.ru',
                    to=[subscriber.user.email],
                )
                html_content = render_to_string(
                    'weeklysubscribeletter.html',
                    {
                        'new': post,
                        'recipient': subscriber.user
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


@shared_task
def check_new(sender, **kwargs):
    if len(Post.objects.filter(publishing_date__gt=(datetime.date.today() - datetime.timedelta(seconds=1.5)))) != 0:
        for post in Post.objects.filter(publishing_date__gt=(datetime.date.today() - datetime.timedelta(seconds=1.5))):
            for cat in PostCategory.objects.filter(post=post):
                for subscriber in Subscribers.objects.filter(category=cat.categories):
                    msg = EmailMultiAlternatives(
                        subject=post.title,
                        body=post.content,
                        from_email='yv9v@yandex.ru',
                        to=[subscriber.user.email],
                    )
                    html_content = render_to_string(
                        'newpostsubscribeletter.html',
                        {
                            'new': post,
                            'recipient': subscriber.user
                        }
                    )

                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
    else:
        pass
