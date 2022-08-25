from django.contrib.auth.models import User
from django.db import models


class Adv(models.Model):
    TANKS = 'Танки'
    HEALERS = 'Хилы'
    DMG = 'ДД'
    TRADERS = 'Торговцы'
    GUILDMASTERS = 'Гилдмастеры'
    QUESTGIVERS = 'Квестгиверы'
    SMITHS = 'Кузнецы'
    LEATHERMEN = 'Кожевники'
    POTIONMAKERS = 'Зельевары'
    WIZARDS = 'Мастера заклинаний'
    guild_types = [
        (TANKS, 'Танки'), (HEALERS, 'Хилы'), (DMG, 'ДД'), (TRADERS, 'Торговцы'),
        (GUILDMASTERS, 'Гилдмастеры'), (QUESTGIVERS, 'Квестгиверы'), (SMITHS, 'Кузнецы'),
        (LEATHERMEN, 'Кожевники'), (POTIONMAKERS, 'Зельевары'), (WIZARDS, 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    guild = models.CharField(max_length=64, choices=guild_types, default=TANKS)
    title = models.CharField(max_length=256)
    content = models.FileField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title[:25]}'


class AdvReply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    adv = models.ForeignKey(Adv, on_delete=models.CASCADE)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class OneTimeCode(models.Model):
    codeUser = models.OneToOneField(User, on_delete=models.CASCADE)
    oneTimeCode = models.CharField(max_length=128)
