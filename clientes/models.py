from django.db import models
from django.conf import settings


class Cliente(models.Model):
    """
    Entidade principal do cliente (Seção 9.2).
    Centraliza os dados básicos e diferencia PF de PJ.
    """

    class Tipo(models.TextChoices):
        FISICA = 'PF', 'Pessoa Física'
        JURIDICA = 'PJ', 'Pessoa Jurídica'

    tipo = models.CharField(
        max_length=2,
        choices=Tipo.choices,
        default=Tipo.FISICA,
        verbose_name='Tipo de Pessoa'
    )

    # Nome ou Razão Social
    nome = models.CharField(max_length=255, verbose_name='Nome Completo / Razão Social')

    # Nome Fantasia (apenas para PJ, mas opcional para todos para simplificar banco)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')

    cpf_cnpj = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='CPF / CNPJ',
        help_text='Insira apenas números'
    )

    rg_ie = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='RG / Inscrição Estadual'
    )

    # Contatos principais
    telefone = models.CharField(max_length=20, verbose_name='Telefone Principal')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')

    # Vínculo com Técnico Responsável (Seção 9.2 - Regra Obrigatória)
    tecnico_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_atendidos',
        verbose_name='Técnico Responsável',
        limit_choices_to={'role': 'TECNICO'}  # Filtra apenas usuários técnicos no admin
    )

    observacoes = models.TextField(blank=True, verbose_name='Observações Gerais')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Endereco(models.Model):
    """
    Suporte a Múltiplos Endereços (Seção 9.2).
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')

    descricao = models.CharField(
        max_length=50,
        default='Principal',
        verbose_name='Descrição do Local',
        help_text='Ex: Casa, Escritório, Loja Centro'
    )

    logradouro = models.CharField(max_length=255, verbose_name='Rua/Av')
    numero = models.CharField(max_length=20, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='BA', verbose_name='UF')
    cep = models.CharField(max_length=10, verbose_name='CEP')

    referencia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ponto de Referência')

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f"{self.descricao} - {self.logradouro}, {self.numero}"


class ContatoSecundario(models.Model):
    """
    Contatos familiares ou adicionais vinculados (Seção 9.2).
    Útil para recados ou responsáveis financeiros em empresas.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos_secundarios')

    nome = models.CharField(max_length=100, verbose_name='Nome do Contato')
    cargo_parentesco = models.CharField(
        max_length=50,
        verbose_name='Cargo / Parentesco',
        help_text='Ex: Esposa, Gerente, Vizinho'
    )
    telefone = models.CharField(max_length=20, verbose_name='Telefone')

    class Meta:
        verbose_name = 'Contato Secundário'
        verbose_name_plural = 'Contatos Secundários'

    def __str__(self):
        return f"{self.nome} ({self.cargo_parentesco})"
