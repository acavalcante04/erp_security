from django.db import models
from datetime import date
from dateutil.relativedelta import \
    relativedelta  # Precisaremos instalar se não tiver, mas usaremos lógica simples primeiro


class Categoria(models.Model):
    """
    Categorias de produtos criadas pelo administrador.
    Ex: Câmeras, Cabos, Sensores, Serviços de Mão de Obra.
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome da Categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Cadastro central de Produtos e Serviços (Seção 9.3).
    """

    class Tipo(models.TextChoices):
        PRODUTO = 'P', 'Produto Físico'
        SERVICO = 'S', 'Serviço (Mão de Obra)'

    tipo = models.CharField(
        max_length=1,
        choices=Tipo.choices,
        default=Tipo.PRODUTO,
        verbose_name='Tipo do Item'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        verbose_name='Categoria'
    )

    nome = models.CharField(max_length=255, verbose_name='Nome do Produto/Serviço')

    # Preços
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Preço de Custo')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Preço de Venda')

    # Controle de Estoque
    quantidade = models.IntegerField(default=0, verbose_name='Quantidade em Estoque')
    estoque_minimo = models.IntegerField(default=5, verbose_name='Estoque Mínimo (Alerta)')

    # Identificação e Localização
    codigo_barras = models.CharField(max_length=100, blank=True, null=True, unique=True,
                                     verbose_name='Código de Barras / GTIN')
    referencia_fabricante = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cód. Fabricante')
    local_fisico = models.CharField(max_length=100, blank=True, null=True, verbose_name='Localização no Estoque',
                                    help_text='Ex: Prateleira A1, Gaveta 2')
    garantia_meses = models.IntegerField(
        default=3,
        verbose_name='Garantia (Meses)',
        help_text='Tempo de garantia oferecido ao cliente (ex: 3, 12, 24)'
    )

    # Rastreabilidade e Validade
    controlar_num_serie = models.BooleanField(default=False, verbose_name='Exigir Nº Série na Venda?')
    validade = models.DateField(blank=True, null=True, verbose_name='Data de Validade (se aplicável)')

    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto / Serviço'
        verbose_name_plural = 'Produtos e Serviços'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    @property
    def alerta_promocao(self):
        # ... (Mantenha a lógica do alerta_promocao igual) ...
        if self.tipo == self.Tipo.SERVICO:
            return False
        hoje = date.today()
        data_cadastro_date = self.data_cadastro.date()
        idade_anos = relativedelta(hoje, data_cadastro_date).years
        return idade_anos >= 2