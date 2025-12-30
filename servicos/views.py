from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from weasyprint import HTML
from core.models import ConfiguracaoSistema
from .models import Orcamento, OrdemServico


@staff_member_required
def gerar_orcamento_pdf(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    config = ConfiguracaoSistema.objects.first()

    if not config:
        config = {'nome_empresa': 'Configure no Admin', 'endereco_completo': ''}

    context = {
        'orcamento': orcamento,
        'itens': orcamento.itens.all(),
        'config': config,
        'request': request
    }

    html_string = render_to_string('servicos/orcamento_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"orcamento_{orcamento.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


@staff_member_required
def gerar_os_pdf(request, pk):
    """
    Gera o PDF da Ordem de Serviço.
    Se a OS veio de um Orçamento, busca os itens dele para exibir.
    """
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    config = ConfiguracaoSistema.objects.first()

    if not config:
        config = {'nome_empresa': 'Configure no Admin', 'endereco_completo': ''}

    # Busca itens se houver orçamento de origem
    itens = []
    if os_obj.orcamento_origem:
        itens = os_obj.orcamento_origem.itens.all()

    context = {
        'os': os_obj,
        'itens': itens,
        'config': config,
        'request': request
    }

    html_string = render_to_string('servicos/os_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"os_{os_obj.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


@staff_member_required
def gerar_garantia_pdf(request, pk):
    """
    Gera o Termo de Garantia com base na OS finalizada.
    Lista os produtos e seus respectivos prazos de garantia cadastrados no Estoque.
    """
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    config = ConfiguracaoSistema.objects.first()

    if not config:
        config = {'nome_empresa': 'Configure no Admin', 'endereco_completo': ''}

    # Busca itens do orçamento de origem
    itens = []
    if os_obj.orcamento_origem:
        itens = os_obj.orcamento_origem.itens.all()

    context = {
        'os': os_obj,
        'itens': itens,
        'config': config,
        'request': request
    }

    html_string = render_to_string('servicos/garantia_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"garantia_os_{os_obj.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response