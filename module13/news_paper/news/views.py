from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from news.filters import PostFilter
from news.forms import PostForm, UserForm, SubscribeForm
from news.models import Post, PostCategory, Subscribers


class PostList(ListView):
    model = Post
    ordering = ['-publishing_date']
    template_name = 'news/news_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_cats'] = PostCategory.objects.filter(posts__pk=context['post'].pk)
        context['subscriptions'] = Subscribers.objects.filter(user=self.request.user)
        return context


class PostSearch(ListView):
    model = Post
    ordering = ['-publishing_date']
    template_name = 'news/news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'News'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'News'
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'Articles'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'Articles'
        return super().form_valid(form)


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'news/user_edit.html'


class CreateSubscribeView(LoginRequiredMixin, CreateView):
    form_class = SubscribeForm
    model = Subscribers
    template_name = 'subscribe.html'
    success_url = '/news/subscribe/'

    def form_valid(self, form):
        form.instance.subscriber = User.objects.get(id=self.request.user.id)
        if Subscribers.objects.filter(category=form.instance.category, user=form.instance.subscriber):
            return super(CreateSubscribeView, self).form_invalid(form)
        else:
            return super(CreateSubscribeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mysubscribes'] = Subscribers.objects.filter(user=User.objects.get(id=self.request.user.id))
        return context


class UnSubscribeView(LoginRequiredMixin, DeleteView):
    model = Subscribers
    template_name = 'unsubscribe.html'
    success_url = reverse_lazy('subscription')
    context_object_name = 'sub'

