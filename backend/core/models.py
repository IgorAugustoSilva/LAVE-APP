from django.db import models
from localflavor.br.br_states import STATE_CHOICES


class Endereco(models.Model):
    uf = models.CharField(
        'UF',
        max_length=2,
        choices=STATE_CHOICES,
        default='MG'
    )
    cidade = models.CharField(
        'cidade',
        max_length=100,
        default='Cachoeira de Minas'
    )
    bairro = models.CharField(
        'bairro',
        max_length=100,
        null=True,
        blank=True
    )
    rua = models.CharField(
        'rua',
        max_length=100,
        null=True,
        blank=True
    )
    numero = models.CharField(
        'número', 
        max_length=5, 
        null=True, 
        blank=True
    )
    complemento = models.CharField(
        'complemento',
        max_length=100,
        null=True,
        blank=True
    )
        
    class Meta:
        abstract = True


    def get_full_address(self):
        """Retorna o endereço completo formatado."""
        address_parts = [
            self.rua,
            f'Número {self.numero}' if self.numero else '',self.bairro,
            f'{self.cidade} - {self.uf}' if self.cidade and self.uf else ''
        ]
        return ', '.join(part for part in address_parts if part)
