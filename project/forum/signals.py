from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from project.forum.models import Adv, AdvReply


@receiver(post_save, sender=Adv)
def notify_new_adt(sender, instance, action,  **kwargs):
    if action == 'adv_add':
        for user in User.objects.all():
            if str(Adv.author) != str(user.username):
                msg = EmailMultiAlternatives(
                    subject=instance.adv.title,
                    body=instance.adv.content,
                    from_email='yv9v@yandex.ru',
                    to=[user.email, ],
                )
                html_content = render_to_string(
                    'signals/new_adv.html',
                    {
                        'new': instance.adv,
                        'recipient': user
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


@receiver(post_save, sender=AdvReply)
def notify_new_advrep(sender, instance, action,  **kwargs):
    if action == 'advreply_add':
        for user in User.objects.all():
            if user == instance.adv.author:
                msg = EmailMultiAlternatives(
                    subject=instance.adv.title,
                    body=instance.adv.content,
                    from_email='yv9v@yandex.ru',
                    to=[user.email, ],
                )
                html_content = render_to_string(
                    'signals/new_rep.html',
                    {
                        'new': instance.adv,
                        'recipient': user
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


@receiver(post_save, sender=AdvReply)
def notify_advrep_status(sender, instance, action, **kwargs):
    if action == 'advreply_edit':
        for user in User.objects.all():
            if user == instance.author:
                msg = EmailMultiAlternatives(
                    subject=instance.adv.title,
                    body=instance.adv.content,
                    from_email='yv9v@yandex.ru',
                    to=[user.email, ],
                )
                html_content = render_to_string(
                    'signals/new_rep_stat.html',
                    {
                        'new': instance.adv,
                        'recipient': user
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()
