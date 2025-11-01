from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_file, name="upload_file"),
    path("success/", views.success, name="success"),
    path("download/", views.download_file, name="download_file"),
]
