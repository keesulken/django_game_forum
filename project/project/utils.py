import string
from random import choice

from django.core.exceptions import ObjectDoesNotExist

from project.forum.models import OneTimeCode


def onetime_code_create(user):
    code = ''.join(choice(string.ascii_letters) for x in range(5))
    OneTimeCode.objects.create(oneTimeCode=code, codeUser=user)


def get_onetime_code(user):
    try:
        codeUser = OneTimeCode.objects.get(codeUser__username=user)
    except ObjectDoesNotExist as e:
        return None

    if codeUser:
        return codeUser.oneTimeCode
    else:
        return None
