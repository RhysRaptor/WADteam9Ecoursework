from django.urls import path
from rango import views

app_name = 'rango'
LOGIN_URL = 'rango:login'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
