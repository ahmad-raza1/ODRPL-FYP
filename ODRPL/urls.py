from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abstracts/', views.abstracts, name='abstracts'),
    path('full_papers/', views.full_papers, name='full_papers'),
    path('loader/', views.loader, name='loader'),
]