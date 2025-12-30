from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ConfiguracaoSistema


class CustomUserAdmin(UserAdmin):
    """
    Configuração do Painel Admin para o Usuário Customizado.
    """
    list_display = ('username', 'email', 'first_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Extras', {'fields': ('role', 'phone')}),
    )


# Registra o modelo User
admin.site.register(User, CustomUserAdmin)


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    """
    Admin para configurar Logomarca e Dados da Empresa.
    """
    list_display = ('nome_empresa', 'cnpj', 'contato_telefone')

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False