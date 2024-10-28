from datetime import date
from decimal import Decimal
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from backend.crm.models import Cliente
from backend.servico.models import OrdemServico, OrdemServicoItem, Servico

router = Router()


ServicoSchema = create_schema(Servico, fields=(
    'id',
    'titulo',
))


class OrdemServicoItemSchemaIn(Schema):
    ordem_servico_id: int = None
    servico_id: int
    valor: Decimal
    previsao_entrega: date = None
    tipo: str
    quantidade: Decimal 
    observacao: str = None


class OrdemServicoSchemaIn(Schema):
    situacao: str
    data_coleta: date 
    pagamento: str
    deliver: str
    cliente_id: int
    ordem_servico_itens: List[OrdemServicoItemSchemaIn]


@router.get('servico/', response=List[ServicoSchema])
def list_servico(request, search=None):
    if search:
        return Servico.objects.filter(titulo__istartswith=search)
    return Servico.objects.all()


@router.post('ordem-servico/')
def create_ordem_servico(request, payload: OrdemServicoSchemaIn):
    data = payload.dict()

    situacao = data.get('situacao')
    data_coleta = data.get('data_coleta')
    pagamento = data.get('pagamento')
    deliver = data.get('deliver')
    cliente_id = data.get('cliente_id')

    # Todos são equivalentes
    # cliente = Cliente.objects.get(pk=cliente_id)
    # cliente = Cliente.objects.filter(pk=cliente_id).first()
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    # Cria a OrdemServico
    ordem_servico = OrdemServico.objects.create(situacao=situacao, data_coleta=data_coleta, pagamento=pagamento, deliver=deliver, cliente=cliente)

    # Cria os itens em OrdemServicoItem (lista)
    items = data.get('ordem_servico_itens')
    for item in items:
        servico_id = item.get('servico_id')
        servico = get_object_or_404(Servico, pk=servico_id)

        valor = item.get('valor')

        previsao_entrega = item.get('previsao_entrega')

        tipo = item.get('tipo')

        quantidade = item.get('quantidade')

        observacao = item.get('observacao')

        OrdemServicoItem.objects.create(
            ordem_servico=ordem_servico,
            servico=servico,
            valor=valor,
            previsao_entrega=previsao_entrega,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao,
        )

    return {
        'ordem_servico_id': ordem_servico.pk,
        'status': HTTPStatus.CREATED
    }

@router.post('ordem-servico/{pk}/update')
def ordem_servico_update(request, pk: int, payload: OrdemServicoSchemaIn):
    print("Payload recebido:", payload.dict())
    
    # Obtém a OrdemServico existente
    ordem_servico = get_object_or_404(OrdemServico, pk=pk)
    data = payload.dict()

    # Atualiza apenas os campos deliver, situacao e pagamento
    ordem_servico.situacao = data.get('situacao')
    ordem_servico.pagamento = data.get('pagamento')
    ordem_servico.deliver = data.get('deliver')

    # Salva as mudanças no banco de dados
    ordem_servico.save()

    print("Ordem de serviço salva com sucesso:", ordem_servico.pk)

    return {
        'ordem_servico_id': ordem_servico.pk,
        'status': HTTPStatus.OK
    }