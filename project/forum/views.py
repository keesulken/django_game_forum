from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AdvForm, AdvReplyForm, AdvReplyStatusForm
from .models import Adv, AdvReply


class AdvList(ListView):
    model = Adv
    ordering = "publishing_date"
    template_name = 'forum/advlist.html'
    context_object_name = 'advs'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class AdvDetail(LoginRequiredMixin, DetailView):
    model = Adv
    ordering = "publishing_date"
    template_name = 'forum/advdetail.html'
    context_object_name = 'adv'


class AdvCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('forum.add_adv',)
    form_class = AdvForm
    model = Adv
    template_name = 'forum/adv_edit.html'

    def form_valid(self, form):
        return super().form_valid(form)


class AdvUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('forum.change_adv',)
    form_class = AdvForm
    model = Adv
    template_name = 'forum/adv_edit.html'

    def form_valid(self, form):
        return super().form_valid(form)


class AdvDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('forum.delete_adv',)
    model = Adv
    template_name = 'forum/adv_delete.html'
    success_url = reverse_lazy('home')


class AdvReplyList(PermissionRequiredMixin, ListView):
    permission_required = ('forum.view_advreply',)
    model = AdvReply
    ordering = "publishing_date"
    template_name = 'forum/advreplylist.html'
    context_object_name = 'advreps'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class AdvReplyCreate(LoginRequiredMixin, CreateView):
    form_class = AdvReplyForm
    model = AdvReply
    success_url = reverse_lazy('home')
    template_name = 'forum/advreplycreate.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return super().form_valid(form)


class AdvReplyChangeStatus(LoginRequiredMixin, UpdateView):
    form_class = AdvReplyStatusForm
    model = AdvReply
    template_name = 'forum/advreply_edit.html'

    def form_valid(self, form):
        return super().form_valid(form)
