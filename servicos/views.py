from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from weasyprint import HTML
from .models import Orcamento
from core.models import ConfiguracaoSistema


@staff_member_required
def gerar_orcamento_pdf(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)

    # Busca as configurações da empresa (Logo, Endereço, etc)
    config = ConfiguracaoSistema.objects.first()

    # Se não tiver configuração salva, cria um objeto vazio para não dar erro
    if not config:
        config = {'nome_empresa': 'Configure no Admin', 'endereco_completo': ''}

    context = {
        'orcamento': orcamento,
        'itens': orcamento.itens.all(),
        'config': config,  # <--- Enviamos a configuração para o HTML
        'request': request  # Necessário para pegar a URL completa da imagem
    }

    html_string = render_to_string('servicos/orcamento_pdf.html', context)

    # base_url=request.build_absolute_uri() é CRUCIAL para carregar a imagem da Logo
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"orcamento_{orcamento.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response


@staff_member_required
def gerar_orcamento_pdf(request, pk):
    """
    Gera o PDF do orçamento para impressão ou envio.
    Apenas usuários logados (staff) podem acessar.
    """
    # 1. Busca o orçamento ou retorna erro 404 se não existir
    orcamento = get_object_or_404(Orcamento, pk=pk)

    # 2. Define o contexto (dados que vão para o HTML)
    context = {
        'orcamento': orcamento,
        'itens': orcamento.itens.all(),
        'empresa': {
            'nome': 'Segurança Eletrônica Exemplo Ltda',
            'telefone': '(11) 99999-9999',
            'email': 'contato@exemplo.com.br'
        }
    }

    # 3. Renderiza o HTML usando um template (que criaremos a seguir)
    html_string = render_to_string('servicos/orcamento_pdf.html', context)

    # 4. Converte o HTML para PDF usando WeasyPrint
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    # 5. Prepara a resposta HTTP para o navegador entender que é um PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')

    # Define o nome do arquivo no download (ex: orcamento_15.pdf)
    filename = f"orcamento_{orcamento.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response