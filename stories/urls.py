from django.urls import path
from . import views


app_name = "stories"


urlpatterns = [
    path('get-user-story', views.get_user_story),
    path('get-stories', views.get_stories),
    path("upload-story", views.upload_story),

]