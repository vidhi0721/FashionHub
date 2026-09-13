from django.urls import path
from . import views

urlpatterns = [
    path("", views.style_assistant, name="style_assistant"),
]