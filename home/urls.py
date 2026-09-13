from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/',views.edit_profile,name='edit_profile'),
]