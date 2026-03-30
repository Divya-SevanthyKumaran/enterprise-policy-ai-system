from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.run_query, name='ask'),
    path('clear/', views.clear_chat, name='clear-chat')
]
