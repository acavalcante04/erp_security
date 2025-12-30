from django.urls import path
from . import views

urlpatterns = [
    # Caminho: /servicos/orcamento/1/pdf/
    path('orcamento/<int:pk>/pdf/', views.gerar_orcamento_pdf, name='orcamento_pdf'),
]