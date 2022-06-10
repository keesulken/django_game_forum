from django.urls import path
from news.views import *

urlpatterns = [
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search', PostSearch.as_view(), name='post_search'),
    path('news/create', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('articles/create', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('profile/<int:pk>/', UserUpdate.as_view(), name='user_edit'),
]
