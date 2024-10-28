from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.http import HttpResponse
import csv
from .forms import OrdemServicoForm, OrdemServicoUpdateForm
from .models import OrdemServico, Servico


def login_view(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("core:index")
    else: 
        form = AuthenticationForm()
    return render(request, "servico/login.html", { "form": form })

def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        return redirect('servico:servico_list')

@login_required(login_url="/servico/login/")
def ordem_servico_list(request):
    template_name = 'servico/ordem_servico_list.html'
    object_list = OrdemServico.objects.all()

    # Filtrar por situação
    search = request.GET.get('search')
    if search:
        object_list = object_list.filter(situacao=search)

    # Filtrar por data de coleta
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    if data_inicio and data_fim:
        object_list = object_list.filter(data_coleta__range=[data_inicio, data_fim])

    context = {
        'object_list': object_list,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, template_name, context)


def export_ordem_servico(request):
    # Filtro por data, se fornecido
    data_inicio = request.GET.get('data_inicio', None)
    data_fim = request.GET.get('data_fim', None)

    ordens_servico = OrdemServico.objects.all()

    if data_inicio and data_fim:
        ordens_servico = ordens_servico.filter(data_coleta__range=[data_inicio, data_fim])

    # Configurando a resposta para o CSV
    response = HttpResponse(content_type='text/csv')
    # Formatação do nome do arquivo com as datas filtradas
    filename = f"ordens_servico_{data_inicio or 'inicio'}_to_{data_fim or 'fim'}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Cliente', 'Data de Coleta', 'Situação', 'Pagamento', 'Entrega'])

    for ordem in ordens_servico:
        writer.writerow([
            ordem.id,
            ordem.cliente.nome,
            ordem.data_coleta,
            ordem.get_situacao_display(),
            ordem.get_pagamento_display(),
            'Sim' if ordem.deliver == 'sim' else 'Não'
        ])

    return response

def ordem_servico_create(request):
    template_name = 'servico/ordem_servico_form.html'

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            # O campo 'deliver' deve ser tratado corretamente
            ordem_servico = form.save(commit=False)
            ordem_servico.deliver = form.cleaned_data.get('deliver', False)
            ordem_servico.save()
            return redirect('servico:ordem_servico_detail', pk=ordem_servico.pk)
    else:
        form = OrdemServicoForm()

    context = {'form': form}
    return render(request, template_name, context)


def ordem_servico_detail(request, pk):
    template_name = 'servico/ordem_servico_detail.html'
    instance = OrdemServico.objects.get(pk=pk)
    context = {'object': instance}
    return render(request, template_name, context)


def ordem_servico_update(request, pk):
    instance = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        form = OrdemServicoUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            ordem_servico = form.save(commit=False)
            # Atualiza o campo 'deliver' com base nos dados do formulário
            ordem_servico.deliver = form.cleaned_data.get('deliver')
            ordem_servico.save()
            return redirect('servico:ordem_servico_detail', pk=instance.pk)
    else:
        form = OrdemServicoUpdateForm(instance=instance)

    context = {'form': form}
    return render(request, 'servico/ordem_servico_update_form.html', context)

def ordem_servico_delete(request, pk):
    ...


class ServicoDetailView(DetailView):
    model = Servico


class ServicoListView(ListView):
    model = Servico
    template_name = 'servico/servico_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(titulo__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_ids'] = [46, 47, 48, 54]
        return context


