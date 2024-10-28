from django.contrib import admin

from .models import OrdemServico, OrdemServicoItem, Servico


class OrdemServicoItemInline(admin.TabularInline):
    model = OrdemServicoItem
    extra = 0


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    inlines = (OrdemServicoItemInline,)
    list_display = ('__str__', 'cliente', 'situacao', 'pagamento', 'data_coleta', 'deliver')
    list_display_links = ('cliente',)
    search_fields = ('cliente__nome', 'data_coleta')
    list_filter = ('situacao', 'data_coleta', 'deliver', 'pagamento')


admin.site.register(Servico)
