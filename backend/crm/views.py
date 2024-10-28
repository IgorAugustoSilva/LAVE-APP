from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .forms import ClienteForm
from .models import Cliente

@method_decorator(login_required(login_url='/servico/login/'), name='dispatch')
class ClienteListView(ListView):
    model = Cliente
    paginate_by = 20

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nome__icontains=search)
                | Q(bairro__icontains=search)
                | Q(cidade__icontains=search)
            )
        return qs


class ClienteDetailView(DetailView):
    model = Cliente


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('crm:cliente_list') # Redireciona para a lista de clientes após a atualização


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('crm:cliente_list')  # Redireciona para a lista de clientes após a atualização


# class ClienteDeleteView(DeleteView):
#     model = Cliente
#     success_url = reverse_lazy('crm:cliente_list')
