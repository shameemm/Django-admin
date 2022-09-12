from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
]