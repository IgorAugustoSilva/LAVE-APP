import locale
from datetime import date
from decimal import Decimal
from django.db import models

from backend.crm.models import Cliente


class Servico(models.Model):
    titulo = models.CharField('Título', max_length=100)
    preco_only_view_lavar = models.CharField('Lavar', max_length=6, default='999')
    preco_only_view_lavarpassar = models.CharField('Lavar e Passar', max_length=6, default='999')
    preco_only_view_passar = models.CharField('Passar', max_length=6, default='999')

    class Meta:
        ordering = ('titulo',)
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'

    def __str__(self):
        return f'{self.titulo}'


SITUACAO = (
    ('la', 'Lavando'),
    ('pc', 'Pendente coleta'),
    ('pe', 'Pendente entrega'),
    ('en', 'Entregue'),
)

PAGAMENTO = (
    ('pix', 'Pix'),
    ('din', 'Dinheiro'),
    ('nao', 'Não pago'),
)

DELIVERY_CHOICES = (
    ('sim', 'Sim'),
    ('nao', 'Não'),
)
class OrdemServico(models.Model):
    situacao = models.CharField('Situação', max_length=2, choices=SITUACAO)
    pagamento = models.CharField('Pagamento', max_length=3, choices=PAGAMENTO)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        verbose_name='cliente',
        related_name='ordem_servicos',
        null=True,
        blank=False
    )
    data_coleta = models.DateField('Data de coleta', default=date(2024, 1, 1), null=False, blank=False)
    created = models.DateTimeField(
        'criado em' ,
        auto_now_add=True,
        auto_now=False
    )
    deliver = models.CharField('Entrega', max_length=3, choices=DELIVERY_CHOICES)

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'ordem de serviço'
        verbose_name_plural = 'ordens de serviço'

    def __str__(self):
        return f'{self.pk}'
    
    def get_valor_total_display(self):
        # Calcula o valor total da ordem de serviço
        total = sum((item.valor or 0) * (item.quantidade or 1) for item in self.ordem_servico_itens.all())

        # Formata o total para o formato de moeda brasileiro (R$)
        formatted_total = f"{total:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        
        return f'R$ {formatted_total}' if total else 'R$ 0,00'



TIPO = (
    ('sl', 'Só lavar'),
    ('lp', 'Lavar e passar'),
    ('sp', 'Só passar'),
    ('na', 'Não se aplica'),
)


class OrdemServicoItem(models.Model):
    tipo = models.CharField('Tipo', default="na", max_length=2, choices=TIPO, null=False, blank=False)
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        verbose_name='ordem de serviço',
        related_name='ordem_servico_itens',
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        verbose_name='serviço',
        related_name='ordem_servico_item_servicos',
        null=False, blank=False
    )
    valor = models.DecimalField('valor', default=Decimal(0), max_digits=8, decimal_places=2, null=False, blank=True)
    previsao_entrega = models.DateField('Previsão de entrega', null=True, blank=True)
    quantidade = models.DecimalField('quantidade', default=Decimal(0), max_digits=8, decimal_places=2, null=False, blank=False)  # deixado em decimal com duas casas para caluclo de metro2 do tapete
    observacao = models.TextField('Observação', null=True, blank=True)

    class Meta:
        ordering = ('-pk',)  # ordem decrescente, se quiser crescente só tirar o sinal de menos.
        verbose_name = 'item da ordem de serviço'
        verbose_name_plural = 'itens da ordens de serviço'

    def get_valor_total_item(self):
        total = (self.valor or 0) * (self.quantidade or 1)  # Calculate the total value for the item

        # Formatar o valor manualmente, estilo brasileiro (ex: 1.234,56)
        formatted_total = f'{total:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')
    
        return f'R$ {formatted_total}' if total else 'R$ 0,00'
    
    def quantidade_m2(self):
        titulo_servico = self.servico.titulo.lower()  # Convert to lowercase for case-insensitive comparison
        if "tapete" in titulo_servico or "cortina" in titulo_servico:
            return f"{self.quantidade} m²"
        return self.quantidade

    def __str__(self):
        return f'{self.pk}'
