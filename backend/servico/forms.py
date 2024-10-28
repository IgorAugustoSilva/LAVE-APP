from django import forms
from .models import OrdemServico, OrdemServicoItem

class OrdemServicoForm(forms.ModelForm):
    # Campos adicionais que não estão diretamente no modelo OrdemServico
    servico = forms.CharField(required=True)
    valor = forms.DecimalField(required=True)
    tipo = forms.CharField(required=True)
    quantidade = forms.DecimalField(required=True)
    observacao = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        required=False
    )

    # Campos relacionados ao modelo OrdemServico
    data_coleta = forms.DateField(
        label='Data de coleta',
        required=True,
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%d-%m-%Y',),
    )
    previsao_entrega = forms.DateField(
        label='Previsão de entrega',
        required=True,
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%d-%m-%Y',),
    )
    deliver = forms.ChoiceField(
        label='Entrega',
        required=True,
        widget=forms.RadioSelect,
    )
    
    def clean_deliver(self):
        return self.cleaned_data.get('deliver', 'nao')
    class Meta:
        model = OrdemServico
        fields = ['situacao', 'pagamento', 'cliente', 'data_coleta', 'previsao_entrega', 'deliver']

class OrdemServicoUpdateForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['situacao', 'pagamento', 'deliver']
