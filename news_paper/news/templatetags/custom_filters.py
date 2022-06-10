# почему-то как бы я не колдовал с пакетами templatetags и путями, фильтр django все равно ищет в
# simpleapp/templatetags
# Здесь для наглядности фильтр из задания, но работает он именно оттуда)
# Как по мне, написаный фильтр получается очень ресурсоёмкий и в реальной ситуации вряд ли был бы взят на вооружение,
# но более изящного рещения я так сразу не придумал.


import re

from django import template

from news.exceptions import FilterValueError

register = template.Library()


@register.filter()
def censor(text):
    if type(text) == str:
        censor_template = r'[Пп]иво|[Кк]атастроф|[Кк]онфликт|[Кк]рот|[Бб]утырка'
        for i in re.finditer(censor_template, text):
            censored_line = "*"*(i.span()[1] - i.span()[0])
            text = text.replace(i.group(0), censored_line)
        return text
    else:
        raise FilterValueError

