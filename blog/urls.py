from django.urls import path
from .views import post_delete, post_create, post_detail, post_update, PostList, post_list

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='index'),
    path('post/create/', post_create, name='post_create'),
    path('post/update/<int:post_id>', post_update, name='post_update'),
    path('post/delete/<int:post_id>', post_delete, name='post_delete'),
    path('post/detail/<int:post_id>', post_detail, name='post_detail'),
]