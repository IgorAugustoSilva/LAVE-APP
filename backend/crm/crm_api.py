from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.crm.models import Cliente

router = Router()

ClienteSchema = create_schema(Cliente, fields=(
    'id',
    'nome',
    'rua',
    'numero',
    'bairro',
))


@router.get('cliente/', response=List[ClienteSchema])
def list_cliente(request, search=None):
    if search:
        return Cliente.objects.filter(nome__istartswith=search)
    return Cliente.objects.all()
