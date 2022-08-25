from django.urls import path, include

from .views import AdvList, AdvDetail, AdvReplyCreate, AdvCreate, AdvUpdate, AdvDelete, AdvReplyList

urlpatterns = [
    path('', AdvList.as_view(), name='home'),
    path('<int:pk>', AdvDetail.as_view()),
    path('reply/', AdvReplyCreate.as_view()),
    path('create/<int:pk>', AdvCreate.as_view()),
    path('update/<int:pk>', AdvUpdate.as_view()),
    path('delete/<int:pk>', AdvDelete.as_view()),
    path('profile/', AdvReplyList.as_view()),
]
