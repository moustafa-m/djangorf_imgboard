from django.urls import path
from . import views

urlpatterns = [
    path('post/list/', views.PostList.as_view(), name='post_list'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetails.as_view(), name='post_details'),
]