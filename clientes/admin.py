from django.contrib import admin
from .models import Cliente, Endereco, ContatoSecundario


class EnderecoInline(admin.TabularInline):
    """
    Permite editar endereços dentro da tela do cliente.
    """
    model = Endereco
    extra = 0
    can_delete = True
    classes = ['collapse']


class ContatoSecundarioInline(admin.TabularInline):
    """
    Permite editar contatos secundários dentro da tela do cliente.
    """
    model = ContatoSecundario
    extra = 0
    can_delete = True


class ClienteAdmin(admin.ModelAdmin):
    """
    Configuração principal do Admin de Clientes.
    """
    # Colunas visíveis na lista (Aqui métodos funcionam)
    list_display = ('nome', 'tipo', 'telefone', 'tecnico_responsavel', 'cidade_principal')

    # Filtros laterais (CORREÇÃO: Usando campo direto do relacionamento)
    # 'enderecos__estado' navega até a tabela Endereco e filtra pelo campo estado
    list_filter = ('tipo', 'enderecos__estado', 'tecnico_responsavel')

    # Campo de busca
    search_fields = ('nome', 'cpf_cnpj', 'telefone', 'email')

    # Adiciona as tabelas filhas
    inlines = [EnderecoInline, ContatoSecundarioInline]

    # Organização dos campos no formulário
    fieldsets = (
        ('Dados Principais', {
            'fields': ('tipo', 'nome', 'nome_fantasia', 'cpf_cnpj', 'rg_ie')
        }),
        ('Contato Principal', {
            'fields': ('telefone', 'email', 'tecnico_responsavel')
        }),
        ('Outros', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    # Métodos auxiliares para mostrar dados na LISTA (Visual apenas)
    def cidade_principal(self, obj):
        endereco = obj.enderecos.first()
        return f"{endereco.cidade}/{endereco.estado}" if endereco else "-"

    cidade_principal.short_description = 'Cidade/UF'


# Registro final
admin.site.register(Cliente, ClienteAdmin)