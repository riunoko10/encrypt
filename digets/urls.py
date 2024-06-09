from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hash/', views.hash, name='hash'),
    path('md5/', views.md5, name='md5'),
    path('rc4/', views.rc4, name='rc4'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user/<str:username>', views.user, name='user'),
    
]