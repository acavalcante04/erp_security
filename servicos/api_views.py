from rest_framework import viewsets
from .models import OrdemServico
from .serializers import OrdemServicoSerializer


class OrdemServicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para listar e ver detalhes das OS no celular.
    ReadOnlyModelViewSet = O celular pode ler (GET), mas ainda não pode apagar.
    """
    queryset = OrdemServico.objects.all().order_by('-data_abertura')
    serializer_class = OrdemServicoSerializer

    # Permite filtrar por status (ex: só as PENDENTES)
    filterset_fields = ['status', 'cliente__nome']