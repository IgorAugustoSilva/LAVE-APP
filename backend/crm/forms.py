from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    telefone = forms.CharField(max_length=18, label='Telefone', required=False)
    CPF = forms.CharField(max_length=11, label='CPF', required=False)

    class Meta:
        model = Cliente
        fields = ('nome', 'CPF', 'telefone', 'uf', 'cidade', 'bairro', 'rua', 'numero', 'complemento')
