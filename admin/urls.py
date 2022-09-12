from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('adminout',views.adminout,name='adminout'),
    path('edituser',views.edituser,name='edituser'),
    path('deleteuser',views.deleteuser,name='deleteuser'),
    path('adduser',views.adduser, name='adduser'),
    
]
