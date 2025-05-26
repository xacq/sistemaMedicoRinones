# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard_patient, name='dashboard_patient'),
    path('profile/edit/', views.patient_profile_edit, name='patient_profile_edit'),
    path('history/', views.patient_history, name='patient_history'),
    path('results/', views.patient_results, name='patient_results'),
    path('exam/<int:pk>/', views.patient_exam_detail, name='patient_exam_detail'),
    path('result/<int:pk>/', views.patient_result_detail, name='patient_result_detail'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('register/', views.register, name='register'),
    path('procesar-imagen/', views.procesar_imagen_view, name='procesar_imagen'),
]
