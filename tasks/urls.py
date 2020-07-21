from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('edit_task/<str:pk>/', views.editTask, name='edit_task'),
    path('delete_task/<str:pk>/', views.deleteTask, name='delete_task'),
    path('downloadPDF', views.downloadPDF, name='download_pdf'),
]
