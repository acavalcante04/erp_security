from decimal import Decimal  # <--- IMPORTAÇÃO ESSENCIAL NOVA
from django.db import models
from django.conf import settings
from clientes.models import Cliente
from estoque.models import Produto


class Orcamento(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = 'RASCUNHO', 'Rascunho'
        ENVIADO = 'ENVIADO', 'Enviado ao Cliente'
        APROVADO = 'APROVADO', 'Aprovado'
        REJEITADO = 'REJEITADO', 'Rejeitado'
        CONVERTIDO = 'CONVERTIDO', 'Virou OS'

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    validade = models.DateField(verbose_name='Válido até')

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RASCUNHO
    )

    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total dos Itens')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Desconto (R$)')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Líquido')

    observacoes = models.TextField(blank=True, verbose_name='Condições de Pagamento / Obs')

    def save(self, *args, **kwargs):
        # CORREÇÃO DO ERRO: Converte tudo para Decimal antes de calcular
        val_bruto = Decimal(str(self.valor_bruto or 0))
        val_desc = Decimal(str(self.desconto or 0))

        self.valor_bruto = val_bruto
        self.desconto = val_desc
        self.valor_total = val_bruto - val_desc

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome}"


class ItemOrcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto/Serviço')

    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Unitário')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Garante cálculo com Decimal também nos itens
        qtd = Decimal(str(self.quantidade))
        preco = Decimal(str(self.preco_unitario))
        self.subtotal = qtd * preco
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


class OrdemServico(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Aguardando Início'
        EM_ANDAMENTO = 'ANDAMENTO', 'Em Execução'
        AGUARDANDO_PECA = 'AG_PECA', 'Aguardando Peça'
        FINALIZADO = 'FINALIZADO', 'Finalizado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    orcamento_origem = models.ForeignKey(
        Orcamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Gerado do Orçamento'
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'TECNICO'},
        verbose_name='Técnico Responsável'
    )

    data_abertura = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)

    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Serviço/Peças')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Desconto (R$)')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Final')

    descricao_problema = models.TextField(verbose_name='Descrição do Problema / Solicitação')
    laudo_tecnico = models.TextField(blank=True, verbose_name='Laudo Técnico / Solução')
    sincronizado = models.BooleanField(default=True, editable=False)

    def save(self, *args, **kwargs):
        # CORREÇÃO DO ERRO: Mesma proteção para a OS
        val_bruto = Decimal(str(self.valor_bruto or 0))
        val_desc = Decimal(str(self.desconto or 0))

        self.valor_bruto = val_bruto
        self.desconto = val_desc
        self.valor_total = val_bruto - val_desc

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente.nome} ({self.get_status_display()})"