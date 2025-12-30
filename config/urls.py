from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas do Módulo de Serviços (PDFs, etc)
    # Qualquer URL que comece com 'servicos/' será enviada para servicos/urls.py
    path('servicos/', include('servicos.urls')),
]