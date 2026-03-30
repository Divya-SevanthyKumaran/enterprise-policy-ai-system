from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('hr_profile', views.hr_profile, name='hr_profile'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile/', views.view_profile, name='profile'),
    path('update/', views.update_profile, name='update'),
    path('users/', views.users_list, name='users_list'),
]
