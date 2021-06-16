from django.urls import path
from . import views

app_name = "webconnect"

urlpatterns = [
    path('get-uuid', views.generate_uuid),
    path('verify-uuid', views.verify_uuid),
]