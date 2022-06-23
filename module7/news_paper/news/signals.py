import datetime

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from models import *
from news.apscheduler import itstime


@receiver(m2m_changed, sender=PostCategory)
def new_post_mailing(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.categories.all():
            for subscriber in Subscribers.objects.filter(category=cat):
                msg = EmailMultiAlternatives(
                    subject=instance.posts.title,
                    body=instance.posts.content,
                    from_email='yv9v@yandex.ru',
                    to=[subscriber.user.email, ],
                )
                html_content = render_to_string(
                    'subscribe_letter.html',
                    {
                        'new': instance.posts,
                        'recipient': subscriber.user
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


@receiver(itstime, sender='Weekly')
def mailing_list2(sender, **kwargs):
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

