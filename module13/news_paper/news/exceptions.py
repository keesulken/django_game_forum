from django.core.exceptions import FieldError


class FilterValueError(FieldError):
    pass
# как своё сообщение об ошибке прикрепить я не разобрался пока
# тест с имитацией ошибке в шаблоне products
