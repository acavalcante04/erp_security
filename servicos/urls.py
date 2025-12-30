from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views # <--- Importante: Importe o arquivo novo

# Configura o Roteador Automático da API
router = DefaultRouter()
router.register(r'ordens', api_views.OrdemServicoViewSet, basename='api_os')

urlpatterns = [
    # --- Rotas de Documentos (PDFs) ---
    path('orcamento/<int:pk>/pdf/', views.gerar_orcamento_pdf, name='orcamento_pdf'),
    path('os/<int:pk>/pdf/', views.gerar_os_pdf, name='os_pdf'),
    path('os/<int:pk>/garantia/', views.gerar_garantia_pdf, name='garantia_pdf'),

    # --- Rota da API (Para o Celular) ---
    # O endereço final será: http://SEU_IP:8000/servicos/api/ordens/
    path('api/', include(router.urls)),
]