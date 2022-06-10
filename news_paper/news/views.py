from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from news.filters import PostFilter
from news.forms import PostForm, UserForm
from news.models import Post


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

