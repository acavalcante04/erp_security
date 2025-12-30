from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ConfiguracaoSistema

class CustomUserAdmin(UserAdmin):
    """
    Configuração do Painel Admin para o Usuário Customizado.
    Herda de UserAdmin para manter a funcionalidade de reset de senha e permissões.
    """

    # Colunas que aparecem na lista de usuários
    list_display = ('username', 'email', 'first_name', 'role', 'is_staff')

    # Filtros laterais (barra direita)
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')

    # Organização dos campos no formulário de EDIÇÃO de usuário
    # Adicionamos a seção 'Informações Extras' com nossos campos personalizados
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('role', 'phone')}),
    )

    # Organização dos campos no formulário de CRIAÇÃO de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Extras', {'fields': ('role', 'phone')}),
    )


# Registra o modelo User com a configuração CustomUserAdmin
admin.site.register(User, CustomUserAdmin)


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    """
    Admin para configurar Logomarca e Dados da Empresa.
    Impede a criação de múltiplas configurações (só deve existir uma).
    """
    list_display = ('nome_empresa', 'cnpj', 'contato_telefone')

    def has_add_permission(self, request):
        # Se já existe 1 registro, bloqueia o botão "Adicionar"
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Bloqueia deletar para não quebrar os PDFs
        return False


class OrcamentoAdmin(admin.ModelAdmin):
    # Atualizado com novas colunas
    list_display = ('id', 'cliente', 'status', 'valor_bruto', 'desconto', 'valor_total', 'botao_imprimir')
    list_filter = ('status', 'validade')
    search_fields = ('cliente__nome', 'id')
    inlines = [ItemOrcamentoInline]
    actions = ['marcar_aprovado', 'gerar_os']

    # Adicionei 'desconto' como editável e os totais como readonly
    readonly_fields = ('valor_bruto', 'valor_total', 'botao_imprimir_formulario')

    fieldsets = (
        ('Dados Básicos', {
            'fields': ('cliente', 'validade', 'status', 'observacoes')
        }),
        ('Financeiro', {
            'fields': ('valor_bruto', 'desconto', 'valor_total')  # Desconto é editável
        }),
        ('Impressão', {
            'fields': ('botao_imprimir_formulario',)
        })
    )