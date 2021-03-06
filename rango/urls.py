from django.urls import path
from rango import views

app_name = 'rango'
LOGIN_URL = 'rango:login'

urlpatterns = [
	path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/upload/', views.add_meme, name='upload'),
    path('like_meme/', views.LikeMemeView.as_view(), name='like_meme'),
    path('dislike_meme/', views.DislikeMemeView.as_view(), name='dislike_meme'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

]
