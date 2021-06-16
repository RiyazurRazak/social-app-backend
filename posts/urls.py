from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path('all-posts', views.index),
    path('explore', views.explore),
    path('add-post', views.add_post),
    path('like/<post_id>', views.like_post),
    path('add-comment', views.add_comment),
    path('comment-reply', views.add_comment_reply),
    path('delete-post/<post_id>', views.delete_post),
    path('delete-comment/<comment_id>', views.delete_comment),
]
