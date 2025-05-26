from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('', views.home, name='home'),
    path('service_list/', views.service_list, name='service_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/new/', views.service_create, name='service_create'),
    path('service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
]
