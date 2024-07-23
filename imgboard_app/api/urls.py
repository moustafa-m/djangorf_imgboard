from django.urls import path
from . import views

urlpatterns = [
    path('post/list/', views.PostList.as_view(), name='post_list'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetails.as_view(), name='post_details'),
    
    path('post/<int:pk>/comments/', views.CommentList.as_view(), name='post_comments'),
    path('post/<int:pk>/comment_create/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment/<int:pk>/', views.CommentDetails.as_view(), name='comment_details'),
]
