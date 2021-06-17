from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_root),
    path('set_webhook/', views.set_webhook, name='set_webhook'),
    path('event/', views.event, name='event'),
    path('users/', views.users, name='users'),
    path('messages/', views.messages, name='messages'),
]
