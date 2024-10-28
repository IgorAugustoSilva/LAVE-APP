from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'telefone', 'rua', 'bairro')
    search_fields = ('nome', 'telefone', 'bairro')
