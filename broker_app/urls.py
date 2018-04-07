from django.urls import path

from broker_app import views

urlpatterns = [
    path('', views.index, name='index'),
]