from rest_framework import serializers
from .models import OrdemServico, ItemOrcamento
from clientes.models import Cliente
from estoque.models import Produto


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # REMOVIDO 'endereco' DA LISTA ABAIXO PARA CORRIGIR O ERRO
        fields = ['id', 'nome', 'telefone', 'cpf_cnpj']


class ProdutoResumidoSerializer(serializers.ModelSerializer):
    """Para mostrar apenas o básico do produto na lista de itens"""

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'tipo', 'preco_venda']


class ItemOSSerializer(serializers.ModelSerializer):
    # Nested Serializer: Traz os dados do produto dentro do item
    produto = ProdutoResumidoSerializer(read_only=True)

    class Meta:
        model = ItemOrcamento
        fields = ['id', 'produto', 'quantidade', 'preco_unitario', 'subtotal']


class OrdemServicoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    itens = serializers.SerializerMethodField()
    tecnico_nome = serializers.CharField(source='tecnico.get_full_name', read_only=True)

    class Meta:
        model = OrdemServico
        fields = [
            'id',
            'cliente',
            'tecnico_nome',
            'status',
            'data_abertura',
            'descricao_problema',
            'laudo_tecnico',
            'valor_total',
            'itens'
        ]

    def get_itens(self, obj):
        """
        Busca os itens do orçamento que originou esta OS.
        """
        if obj.orcamento_origem:
            itens = obj.orcamento_origem.itens.all()
            return ItemOSSerializer(itens, many=True).data
        return []