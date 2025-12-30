from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de Usuário Customizado (Seção 9.1).
    Substitui o usuário padrão do Django para permitir campos extras e perfis definidos.
    """

    # Definição dos Perfis de Acesso (Seção 7.2)
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        TECNICO = 'TECNICO', 'Técnico'
        FINANCEIRO = 'FINANCEIRO', 'Financeiro'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TECNICO,
        verbose_name='Perfil de Acesso',
        help_text='Define as permissões gerais do usuário no sistema'
    )

    # Campo útil para comunicação com técnicos (Seção 9.2 - Contato)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone/WhatsApp'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        # Facilita a visualização nos logs e admin: "joao (Técnico)"
        return f"{self.username} ({self.get_role_display()})"


class ConfiguracaoSistema(models.Model):
    """
    Permite ao admin configurar a aparência dos documentos PDF.
    Padrão Singleton (apenas 1 registro ativo).
    """
    nome_empresa = models.CharField(max_length=100, default="Nome da Sua Empresa")
    cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNPJ")

    # Upload da Logomarca
    logo = models.ImageField(
        upload_to='config/logos/',
        blank=True,
        null=True,
        verbose_name="Logomarca do Cabeçalho",
        help_text="Idealmente uma imagem retangular ou quadrada de alta resolução."
    )

    # Dados de Endereço e Contato (Exatamente como no PDF)
    endereco_completo = models.CharField(
        max_length=255,
        default="Rua Exemplo, 123 - Bairro - Cidade/UF",
        verbose_name="Linha de Endereço"
    )

    contato_email = models.EmailField(blank=True, null=True, verbose_name="E-mail de Contato")
    contato_telefone = models.CharField(
        max_length=50,
        default="(XX) 99999-9999",
        verbose_name="Telefones"
    )

    site = models.URLField(blank=True, null=True, verbose_name="Site/Instagram")

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configuração do Sistema"

    def __str__(self):
        return "Configuração Geral da Empresa"

    def save(self, *args, **kwargs):
        # Garante que só exista 1 configuração no banco
        if not self.pk and ConfiguracaoSistema.objects.exists():
            return
        super().save(*args, **kwargs)