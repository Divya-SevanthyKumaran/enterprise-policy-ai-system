from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_policy'),
    path('list/', views.list_documents, name='view_policies'),
    path('update/<int:pk>/', views.update_document, name='update_document'),
    path('delete/<int:pk>/', views.delete_document, name='delete_document'),
]
