from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'account'

urlpatterns = [
    path('all-users', views.index),
    path("register", views.create_user),
    path("login", obtain_auth_token),
    path("logout", views.logout),
    path("current-user", views.current_user_),
    path('delete', views.delete),
    path("profile", views.profile),
    path("add-following", views.add_following),

]
