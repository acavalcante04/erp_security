from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Orcamento, ItemOrcamento, OrdemServico


# 1. Primeiro definimos o Inline (Itens do Orçamento)
class ItemOrcamentoInline(admin.TabularInline):
    model = ItemOrcamento
    extra = 1
    autocomplete_fields = ['produto']
    readonly_fields = ('subtotal',)


# 2. Depois definimos o Admin do Orçamento (que usa o Inline acima)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'valor_bruto', 'desconto', 'valor_total', 'botao_imprimir')
    list_filter = ('status', 'validade')
    search_fields = ('cliente__nome', 'id')
    inlines = [ItemOrcamentoInline]  # <--- Aqui ele chama a classe definida acima
    actions = ['marcar_aprovado', 'gerar_os']

    readonly_fields = ('valor_bruto', 'valor_total', 'botao_imprimir_formulario')

    fieldsets = (
        ('Dados Básicos', {
            'fields': ('cliente', 'validade', 'status', 'observacoes')
        }),
        ('Financeiro', {
            'fields': ('valor_bruto', 'desconto', 'valor_total')
        }),
        ('Impressão', {
            'fields': ('botao_imprimir_formulario',)
        })
    )

    def botao_imprimir(self, obj):
        if obj.id:
            url = reverse('orcamento_pdf', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #79aec8; color: white; padding: 5px 10px; border-radius: 5px;">Imprimir PDF</a>',
                url
            )
        return "-"

    botao_imprimir.short_description = 'Ações'

    def botao_imprimir_formulario(self, obj):
        if obj.id:
            url = reverse('orcamento_pdf', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank">🖨️ Clique aqui para Imprimir este Orçamento</a>',
                url
            )
        return "Salve antes de imprimir"

    botao_imprimir_formulario.short_description = 'Versão para Impressão'

    @admin.action(description='Aprovar Orçamentos Selecionados')
    def marcar_aprovado(self, request, queryset):
        queryset.update(status=Orcamento.Status.APROVADO)

    @admin.action(description='Gerar OS a partir do Orçamento (Aprovados)')
    def gerar_os(self, request, queryset):
        for orcamento in queryset:
            if orcamento.status != Orcamento.Status.APROVADO:
                self.message_user(request, f"Orçamento #{orcamento.id} não está Aprovado. Ignorado.", level='warning')
                continue

            if OrdemServico.objects.filter(orcamento_origem=orcamento).exists():
                self.message_user(request, f"Orçamento #{orcamento.id} já gerou OS. Ignorado.", level='error')
                continue

            OrdemServico.objects.create(
                orcamento_origem=orcamento,
                cliente=orcamento.cliente,
                descricao_problema=f"Serviço derivado do Orçamento #{orcamento.id}. \nCondições: {orcamento.observacoes}",
                status=OrdemServico.Status.PENDENTE,
                tecnico=request.user,
                # Copia valores financeiros iniciais
                valor_bruto=orcamento.valor_bruto,
                desconto=orcamento.desconto,
                valor_total=orcamento.valor_total
            )

            orcamento.status = Orcamento.Status.CONVERTIDO
            orcamento.save()

            self.message_user(request, f"OS gerada com sucesso para Orçamento #{orcamento.id}!", level='success')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        # Recalcula bruto somando os itens
        total_itens = sum(item.subtotal for item in obj.itens.all())
        obj.valor_bruto = total_itens
        # Salva novamente para acionar a lógica de (Bruto - Desconto = Total) do model
        obj.save()


class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tecnico', 'status', 'valor_total')
    list_filter = ('status', 'tecnico', 'data_abertura')
    search_fields = ('cliente__nome', 'descricao_problema', 'id')
    autocomplete_fields = ['cliente', 'tecnico']

    readonly_fields = ('valor_bruto', 'valor_total', 'sincronizado')

    fieldsets = (
        ('Origem', {
            'fields': ('orcamento_origem', 'cliente', 'tecnico')
        }),
        ('Execução', {
            'fields': ('status', 'descricao_problema', 'laudo_tecnico')
        }),
        ('Financeiro', {
            'fields': ('valor_bruto', 'desconto', 'valor_total')
        }),
        ('Datas e Controle', {
            'fields': ('data_finalizacao', 'sincronizado'),
        }),
    )


# 3. Registra tudo no final
admin.site.register(Orcamento, OrcamentoAdmin)
admin.site.register(OrdemServico, OrdemServicoAdmin)