from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import FormOneTimeCode
from .models import BaseRegisterForm
from ..forum.models import OneTimeCode


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class FirstLoginView(generic.CreateView):
    template_name = 'sign/first_login.html'
    form_class = FormOneTimeCode


def register_code(request):

    if request.method == "POST":
        code_request = request.POST['code']
        email = request.POST['email']
        code_user = None
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                code_user = OneTimeCode.objects.get(codeUser=user)
        except ObjectDoesNotExist as e:
            return redirect(f'/first_login/')

        if code_user is not None:
            if code_user.oneTimeCode == code_request:
                code_user.delete()
                return redirect(f'/login/')
            else:
                return redirect(f'/first_login/')