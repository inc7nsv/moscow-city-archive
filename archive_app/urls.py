from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('feedback/', views.feedback, name='feedback'),
    path('register/', views.register, name='register'),
    path('sitemap/', views.sitemap_page, name='sitemap_page'),
]
