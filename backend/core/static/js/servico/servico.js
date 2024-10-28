const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

const getData = () => ({
  clientes: [],
  cliente: {},
  clienteSelecionado: {},
  searchCliente: '',
  servicos: [],
  servico: {},
  servicoSelecionado: {},
  searchServico: '',
  ordemServico: {},
  ordemServicoItem: {},
  currentId: 1,
  ordemServicoItems: [],
  clienteShow: false,
  clienteError: false,
  servicoShow: false,
  servicoError: false,

  init() {
    // watch - monitora as ações
    this.$watch('searchCliente', (newValue) => {
      if (!newValue) this.clientes = [];
      if (newValue.length >= 3) {
        this.getClientes(newValue);
      }
    });
    this.$watch('searchServico', (newValue) => {
      if (!newValue) this.servicos = [];
      if (newValue.length >= 3) {
        this.getServicos(newValue);
      }
    });
  },

  // Quando um cliente é selecionado da lista, atribua o nome ao campo de busca
  getCliente(cliente) {
    this.clienteSelecionado = cliente;
    this.searchCliente = cliente.nome; // Preenche o campo com o nome do cliente selecionado
    this.clienteShow = false; // Esconde a lista de sugestões
  },

  // Busca por clientes com base na entrada do usuário
  getClientes(searchTerm) {
    fetch(`/api/v1/crm/cliente/?search=${searchTerm}`)
      .then(response => response.json())
      .then(data => {
        this.clientes = data;
        this.clienteShow = true;
      });
  },

  // Valida se um cliente foi selecionado
  validateCliente() {
    if (!this.clienteSelecionado.id) {
      this.clienteError = true;
    } else {
      this.clienteError = false;
    }
  },

  getServico(servico) {
    this.servicoSelecionado = servico;
    this.searchServico = servico.titulo;
    this.servicoShow = false;
  },

  getServicos(searchTerm) {
    fetch(`/api/v1/servico/servico/?search=${searchTerm}`)
      .then(response => response.json())
      .then(data => {
        this.servicos = data;
        this.servicoShow = true;
      });
  },

  // Valida se um serviço foi selecionado
  validateServico() {
    if (!this.servicoSelecionado.id) {
      this.servicoError = true; // Exibe erro se nenhum serviço for selecionado
    } else {
      this.servicoError = false;
    }
  },

  addItem() {
    const servico_id = this.servicoSelecionado.id;
    const servico_titulo = this.servicoSelecionado.titulo;
    const valor = this.ordemServicoItem.valor;
    const previsao_entrega = this.ordemServicoItem.previsaoEntrega;
    const tipo = this.ordemServicoItem.tipo;
    const quantidade = this.ordemServicoItem.quantidade;
    const observacao = this.ordemServicoItem.observacao;

    let ordem_servico_item_id = this.currentId++;
    this.ordemServicoItems.push({
      id: ordem_servico_item_id,
      servico_id,
      servico_titulo,
      valor,
      previsao_entrega,
      tipo,
      quantidade,
      observacao
    });
  },

  deleteOrdemServicoItem(id) {
    const indexToRemove = this.ordemServicoItems.findIndex(i => i.id == id);
    this.ordemServicoItems.splice(indexToRemove, 1);
  },

  // Validação adicional para garantir que há pelo menos um item na ordem de serviço
  validateItens() {
    if (this.ordemServicoItems.length === 0) {
      alert("A ordem de serviço deve conter pelo menos um item.");
      return false;
    }
    return true;
  },

  saveData() {
    this.validateCliente(); // Valida o cliente
    this.validateServico(); // Valida o serviço

    if (this.clienteError || this.servicoError) {
      alert("Por favor, selecione Cliente e serviço antes de enviar o formulário.");
      return;
    }

    // Valida se há itens na ordem de serviço
    if (!this.validateItens()) {
      return; // Interrompe o envio se não houver itens
    }

    // Exibe uma mensagem de confirmação antes de prosseguir com o envio
    const confirmation = confirm("Você tem certeza que deseja salvar esta ordem de serviço?");
    if (!confirmation) {
      return; // Interrompe o envio se o usuário clicar em "Cancelar"
    }

    const cliente_id = this.clienteSelecionado.id;
    const situacao = this.ordemServico.situacao;
    const data_coleta = this.ordemServico.dataColeta;
    const pagamento = this.ordemServico.pagamento;
    const deliver = this.ordemServico.deliver; 
    const ordem_servico_itens = this.ordemServicoItems;
    const bodyData = { cliente_id, situacao, data_coleta, pagamento, deliver, ordem_servico_itens };
    fetch('/api/v1/servico/ordem-servico/', {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify(bodyData),
    })
      .then(response => response.json())
      .then(data => {
        const ordem_servico_id = data.ordem_servico_id;
        window.location.href = `/servico/${ordem_servico_id}/`;
      });
  },

  updateOrdemServico(pk) {
    const situacao = this.ordemServico.situacao;
    const pagamento = this.ordemServico.pagamento;
    const deliver = this.ordemServico.deliver;
    const bodyData = { situacao, pagamento, deliver };

    fetch(`/servico/${pk}/update/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(bodyData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const ordem_servico_id = data.ordem_servico_id;
        window.location.href = `/servico/${ordem_servico_id}/`;
    })
    .catch(error => {
        console.error('Erro ao atualizar a ordem de serviço:', error);
    });
  }
  // Outras funções
});
