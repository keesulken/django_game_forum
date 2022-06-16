import re

from django import template

from news.exceptions import FilterValueError

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': '',
    'usd': "$",
}


@register.filter()
def currency(value, code='rub'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value}{postfix}'


@register.filter()
def censor(text):
    if type(text) == str:
        censor_template = r'[Пп]иво|[Кк]атастроф|[Кк]онфликт|[Кк]рот|[Бб]утырка|[Гг]оня'
        for i in re.finditer(censor_template, text):
            censored_line = "*"*(i.span()[1] - i.span()[0])
            text = text.replace(i.group(0), censored_line)
        return text
    else:
        raise FilterValueError


