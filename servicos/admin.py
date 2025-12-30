from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Orcamento, ItemOrcamento, OrdemServico


class ItemOrcamentoInline(admin.TabularInline):
    model = ItemOrcamento
    extra = 1
    autocomplete_fields = ['produto']
    readonly_fields = ('subtotal',)


class OrcamentoAdmin(admin.ModelAdmin):
    # Adicionei 'botao_imprimir' na lista
    list_display = ('id', 'cliente', 'validade', 'status', 'valor_total', 'botao_imprimir')

    list_filter = ('status', 'validade')
    search_fields = ('cliente__nome', 'id')
    inlines = [ItemOrcamentoInline]
    actions = ['marcar_aprovado', 'gerar_os']

    # Adicionei 'botao_imprimir' aqui também para aparecer dentro do formulário
    readonly_fields = ('valor_total', 'botao_imprimir_formulario')

    # --- NOVO: Botão para a LISTA de orçamentos ---
    def botao_imprimir(self, obj):
        if obj.id:  # Só mostra se o orçamento já estiver salvo
            url = reverse('orcamento_pdf', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #79aec8; color: white; padding: 5px 10px; border-radius: 5px;">Imprimir PDF</a>',
                url
            )
        return "-"

    botao_imprimir.short_description = 'Ações'

    # --- NOVO: Botão para DENTRO do formulário (enquanto edita) ---
    def botao_imprimir_formulario(self, obj):
        if obj.id:
            url = reverse('orcamento_pdf', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank">🖨️ Clique aqui para Imprimir este Orçamento</a>',
                url
            )
        return "Salve antes de imprimir"

    botao_imprimir_formulario.short_description = 'Versão para Impressão'

    # ... (Mantenha seus métodos calcular_total_dinamico, marcar_aprovado, gerar_os e save_related iguais) ...
    # Se quiser, posso colar eles aqui novamente para garantir.

    def calcular_total_dinamico(self, obj):
        total = sum(item.subtotal for item in obj.itens.all())
        return f"R$ {total:.2f}"

    calcular_total_dinamico.short_description = "Soma dos Itens"

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
                tecnico=request.user
            )

            orcamento.status = Orcamento.Status.CONVERTIDO
            orcamento.save()

            self.message_user(request, f"OS gerada com sucesso para Orçamento #{orcamento.id}!", level='success')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        total = sum(item.subtotal for item in obj.itens.all())
        obj.valor_total = total
        obj.save()


class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tecnico', 'status', 'data_abertura')
    list_filter = ('status', 'tecnico', 'data_abertura')
    search_fields = ('cliente__nome', 'descricao_problema', 'id')
    autocomplete_fields = ['cliente', 'tecnico']

    fieldsets = (
        ('Origem', {
            'fields': ('orcamento_origem', 'cliente', 'tecnico')
        }),
        ('Status e Execução', {
            'fields': ('status', 'descricao_problema', 'laudo_tecnico')
        }),
        ('Datas', {
            'fields': ('data_finalizacao',),
        }),
    )


admin.site.register(Orcamento, OrcamentoAdmin)
admin.site.register(OrdemServico, OrdemServicoAdmin)