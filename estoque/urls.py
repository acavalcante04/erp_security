from django.urls import path
from . import views

urlpatterns = [
    path('', views.produto_list, name='produto_list'),
]