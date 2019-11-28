from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_endpoint, name='receive_files'),
]