from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rota de Login Customizada
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard como página inicial
    path('', dashboard, name='dashboard'),

    # Apps
    path('servicos/', include('servicos.urls')),
    path('clientes/', include('clientes.urls')), # Descomente quando criar
    path('estoque/', include('estoque.urls')),   # Descomente quando criar
]