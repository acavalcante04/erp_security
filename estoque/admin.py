from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Produto


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


class ProdutoAdmin(admin.ModelAdmin):
    """
    Gestão de Estoque com indicadores visuais.
    """
    # Adicionei 'garantia_meses' na visualização da lista
    list_display = (
        'nome',
        'tipo',
        'categoria',
        'preco_venda',
        'quantidade',
        'garantia_meses',  # <--- NOVO
        'status_estoque',
        'alerta_validade_visual'
    )

    list_filter = ('tipo', 'categoria', 'local_fisico')
    search_fields = ('nome', 'codigo_barras', 'referencia_fabricante')

    # Organização do Formulário
    fieldsets = (
        ('Identificação', {
            'fields': ('tipo', 'categoria', 'nome', 'codigo_barras', 'referencia_fabricante')
        }),
        ('Valores e Estoque', {
            'fields': ('preco_custo', 'preco_venda', 'quantidade', 'estoque_minimo', 'local_fisico')
        }),
        ('Controle e Garantia', {  # <--- Renomeei o título da seção
            # Adicionei 'garantia_meses' aqui para poder editar
            'fields': ('controlar_num_serie', 'validade', 'garantia_meses', 'data_cadastro')
        }),
    )

    readonly_fields = ('data_cadastro',)

    def status_estoque(self, obj):
        """
        Indicador visual de nível de estoque.
        Vermelho se abaixo do mínimo, Verde se ok.
        Não se aplica a Serviços.
        """
        if obj.tipo == Produto.Tipo.SERVICO:
            return "-"

        if obj.quantidade <= obj.estoque_minimo:
            color = 'red'
            msg = 'BAIXO'
            weight = 'bold'
        else:
            color = 'green'
            msg = 'OK'
            weight = 'normal'

        return format_html(
            '<span style="color: {}; font-weight: {}">{} ({})</span>',
            color, weight, obj.quantidade, msg
        )

    status_estoque.short_description = 'Status Estoque'

    def alerta_validade_visual(self, obj):
        """
        Exibe um alerta visual se o produto for antigo (> 2 anos).
        """
        if obj.alerta_promocao:
            return format_html(
                '<span style="color: orange; font-weight: bold;">⚠️ PROMOÇÃO</span>'
            )
        return "Normal"

    alerta_validade_visual.short_description = 'Idade do Estoque'


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)