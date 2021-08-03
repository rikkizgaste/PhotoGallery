from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewImage, name='image'),
    path('add/', views.addImage, name='add'),
    path('edit/<str:pk>', views.editImage, name='edit-img'),
    path('delete/<str:pk>', views.deleteImage, name='delete-img'),
    path('register/', views.register, name='register'),
    path('demo/', views.demo, name='demo'),
]
