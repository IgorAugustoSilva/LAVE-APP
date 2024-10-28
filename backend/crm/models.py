from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy

from backend.core.models import Endereco


class Cliente(Endereco):
    nome = models.CharField('nome', max_length=120, unique=True)
    CPF = models.CharField('CPF', max_length=11, null=True, blank=True)
    #telefone = models.CharField('telefone', max_length=14, null=True, blank=True)
    telefone_validator = RegexValidator(
        regex=r'^\d{2}9\d{4}\d{4}$',
        message='O telefone deve conter somente número precedido do DDD e o 9.'
    )
    telefone = models.CharField('Telefone', validators=[telefone_validator], max_length=11, null=True, blank=True)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return f'{self.nome}'

    def get_absolute_url(self):
        return reverse_lazy('crm:cliente_detail', kwargs={'pk': self.pk})
