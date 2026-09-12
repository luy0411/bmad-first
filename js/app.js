/**
 * Cartinha para o Papai Noel - Lógica Client-Side
 * Validações gentis, sincronização lúdica em tempo real e acessibilidade infantil.
 * Sem dependências externas, sem telemetria e sem alertas nativos intrusivos.
 */

(function () {
  'use strict';

  // Configuração dos textos lúdicos e ícones para cada comportamento
  const COMPORTAMENTO_CONFIG = {
    'Fui muito bonzinho(a)': {
      icon: '😇',
      textoDestaque: 'fui muito bonzinho(a)',
      frase: 'Neste ano, <span id="carta-comportamento" class="destaque-comportamento"><span class="comportamento-icon-inline" aria-hidden="true">😇</span> fui muito bonzinho(a)</span> e me esforcei para fazer o meu melhor com minha família e amigos!'
    },
    'Tentei bastante': {
      icon: '⭐',
      textoDestaque: 'tentei bastante',
      frase: 'Neste ano, <span id="carta-comportamento" class="destaque-comportamento"><span class="comportamento-icon-inline" aria-hidden="true">⭐</span> tentei bastante</span> e a cada dia dei o meu melhor para aprender e ajudar quem amo!'
    },
    'Às vezes fiz travessura': {
      icon: '🍪',
      textoDestaque: 'às vezes fiz travessura',
      frase: 'Neste ano, <span id="carta-comportamento" class="destaque-comportamento"><span class="comportamento-icon-inline" aria-hidden="true">🍪</span> às vezes fiz travessura</span>, mas prometo que meu coração é enorme e vou continuar melhorando!'
    }
  };

  // Mensagens acolhedoras e sem jargões técnicos
  const MENSAGENS_GENTIS = {
    nomeVazio: 'O Papai Noel precisa saber o seu nome para responder a sua cartinha! ✨',
    idadeInvalida: 'Por favor, digite uma idade mágica válida (entre 1 e 120 anos)! 🎂',
    pedidosVazio: 'O Papai Noel quer muito saber os seus pedidos e desejos especiais de Natal! 🎁'
  };

  // Elementos do DOM
  let formCartinha;
  let inputNome;
  let inputIdade;
  let inputCidade;
  let inputPedidos;
  let radiosComportamento;
  let contadorCaracteres;
  let erroNome;
  let erroIdade;
  let erroPedidos;
  let sucessoValidacao;
  let timerDestaquePergaminho = null;

  // Elementos do Pergaminho
  let cartaNome;
  let cartaIdade;
  let cartaCidade;
  let cartaComportamentoContainer;
  let cartaPedidos;
  let cartaAssinatura;
  let cartaData;
  let pergaminhoCarta;

  // Botões
  let btnValidar;
  let btnLimpar;
  let btnIniciar;
  let btnConhecerMagia;

  function formatarDataNatal() {
    try {
      const hoje = new Date();
      const meses = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
      ];
      const dia = hoje.getDate();
      const mes = meses[hoje.getMonth()];
      const ano = hoje.getFullYear();
      return `${dia} de ${mes} de ${ano}`;
    } catch (e) {
      return 'Natal de 2026';
    }
  }

  function obterComportamentoSelecionado() {
    const radioSelecionado = document.querySelector('input[name="comportamento"]:checked');
    if (radioSelecionado && COMPORTAMENTO_CONFIG[radioSelecionado.value]) {
      return radioSelecionado.value;
    }
    return 'Fui muito bonzinho(a)';
  }

  function atualizarComportamentoNaCarta(valorComportamento) {
    const config = COMPORTAMENTO_CONFIG[valorComportamento] || COMPORTAMENTO_CONFIG['Fui muito bonzinho(a)'];
    if (cartaComportamentoContainer) {
      cartaComportamentoContainer.innerHTML = config.frase;
    }

    // Atualiza estado visual ativo nos labels dos cards
    document.querySelectorAll('.card-comportamento').forEach((card) => {
      const radio = card.querySelector('input[type="radio"]');
      if (radio && radio.value === valorComportamento) {
        card.classList.add('ativo');
      } else {
        card.classList.remove('ativo');
      }
    });
  }

  function atualizarPergaminhoAoVivo() {
    const nome = inputNome ? inputNome.value.trim() : '';
    const idadeVal = inputIdade ? inputIdade.value.trim() : '';
    const cidade = inputCidade ? inputCidade.value.trim() : '';
    const pedidos = inputPedidos ? inputPedidos.value.trim() : '';

    if (cartaAssinatura) {
      cartaAssinatura.textContent = nome || '...';
    }

    if (cartaPedidos) {
      if (pedidos) {
        cartaPedidos.textContent = pedidos;
      } else {
        cartaPedidos.textContent = '(Seus desejos e pedidos especiais para o Papai Noel aparecerão aqui com todo o encanto...)';
      }
    }

    const paragrafoApresentacao = document.querySelector('.carta-paragrafo-apresentacao');
    if (paragrafoApresentacao) {
      const nomeHtml = `Meu nome é <strong id="carta-nome" class="destaque-pergaminho">${nome || '...'}</strong>`;
      const cidadeHtml = ` e moro em <strong id="carta-cidade" class="destaque-pergaminho">${cidade || 'uma linda cidade'}</strong>.`;

      if (idadeVal !== '') {
        const numIdade = Number(idadeVal);
        if (!isNaN(numIdade) && numIdade >= 1 && numIdade <= 120 && Number.isInteger(numIdade)) {
          const anosTexto = numIdade === 1 ? 'ano' : 'anos';
          paragrafoApresentacao.innerHTML = `${nomeHtml}, tenho <strong id="carta-idade" class="destaque-pergaminho">${numIdade}</strong> ${anosTexto}${cidadeHtml}`;
        } else {
          paragrafoApresentacao.innerHTML = `${nomeHtml}${cidadeHtml}`;
        }
      } else {
        paragrafoApresentacao.innerHTML = `${nomeHtml}${cidadeHtml}`;
      }

      cartaNome = document.getElementById('carta-nome');
      cartaIdade = document.getElementById('carta-idade');
      cartaCidade = document.getElementById('carta-cidade');
    }
  }

  function exibirErroGentil(inputElem, erroElem, mensagem) {
    if (inputElem) {
      inputElem.classList.add('is-invalid');
      inputElem.setAttribute('aria-invalid', 'true');
    }
    if (erroElem) {
      erroElem.textContent = mensagem;
      erroElem.classList.remove('d-none');
    }
  }

  function limparErroGentil(inputElem, erroElem) {
    if (inputElem) {
      inputElem.classList.remove('is-invalid');
      inputElem.removeAttribute('aria-invalid');
    }
    if (erroElem) {
      erroElem.textContent = '';
      erroElem.classList.add('d-none');
    }
  }

  function limparTodosErros() {
    limparErroGentil(inputNome, erroNome);
    limparErroGentil(inputIdade, erroIdade);
    limparErroGentil(inputPedidos, erroPedidos);
    if (sucessoValidacao) {
      sucessoValidacao.classList.add('d-none');
    }
  }

  function validarFormulario(evento) {
    if (evento) {
      evento.preventDefault();
    }

    limparTodosErros();

    let temErro = false;
    let primeiroElementoComErro = null;

    // 1. Validação do Nome (obrigatório)
    const nomeVal = inputNome ? inputNome.value.trim() : '';
    if (!nomeVal) {
      exibirErroGentil(inputNome, erroNome, MENSAGENS_GENTIS.nomeVazio);
      temErro = true;
      if (!primeiroElementoComErro) {
        primeiroElementoComErro = inputNome;
      }
    }

    // 2. Validação da Idade (opcional, mas se preenchida deve ser número inteiro entre 1 e 120)
    const idadeVal = inputIdade ? inputIdade.value.trim() : '';
    if (idadeVal !== '') {
      const numIdade = Number(idadeVal);
      if (isNaN(numIdade) || numIdade < 1 || numIdade > 120 || !Number.isInteger(numIdade)) {
        exibirErroGentil(inputIdade, erroIdade, MENSAGENS_GENTIS.idadeInvalida);
        temErro = true;
        if (!primeiroElementoComErro) {
          primeiroElementoComErro = inputIdade;
        }
      }
    }

    // 3. Validação dos Pedidos (obrigatório)
    const pedidosVal = inputPedidos ? inputPedidos.value.trim() : '';
    if (!pedidosVal) {
      exibirErroGentil(inputPedidos, erroPedidos, MENSAGENS_GENTIS.pedidosVazio);
      temErro = true;
      if (!primeiroElementoComErro) {
        primeiroElementoComErro = inputPedidos;
      }
    }

    // Tratamento de resultado
    if (temErro) {
      if (sucessoValidacao) {
        sucessoValidacao.classList.add('d-none');
      }
      if (primeiroElementoComErro) {
        // Foco suave no primeiro campo com erro
        primeiroElementoComErro.focus({ preventScroll: false });
        primeiroElementoComErro.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return false;
    }

    // Sucesso na validação: Monta carta final e dá feedback gentil
    atualizarPergaminhoAoVivo();
    atualizarComportamentoNaCarta(obterComportamentoSelecionado());

    if (sucessoValidacao) {
      sucessoValidacao.classList.remove('d-none');
    }

    if (pergaminhoCarta) {
      if (timerDestaquePergaminho) {
        clearTimeout(timerDestaquePergaminho);
        timerDestaquePergaminho = null;
      }
      pergaminhoCarta.classList.remove('pergaminho-destaque');
      void pergaminhoCarta.offsetWidth;
      pergaminhoCarta.classList.add('pergaminho-destaque');
      timerDestaquePergaminho = setTimeout(() => {
        pergaminhoCarta.classList.remove('pergaminho-destaque');
        timerDestaquePergaminho = null;
      }, 1600);

      // Transfere o foco acessível para o pergaminho
      pergaminhoCarta.focus();

      // Em dispositivos móveis, rola suavemente para o pergaminho
      if (window.innerWidth < 992) {
        pergaminhoCarta.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    return true;
  }

  function resetarFormulario() {
    if (formCartinha) {
      formCartinha.reset();
    }
    limparTodosErros();

    // Volta para o comportamento padrão
    const radioBonzinho = document.getElementById('comportamento-bonzinho');
    if (radioBonzinho) {
      radioBonzinho.checked = true;
    }
    atualizarComportamentoNaCarta('Fui muito bonzinho(a)');

    if (contadorCaracteres) {
      contadorCaracteres.textContent = '0/1000';
    }

    atualizarPergaminhoAoVivo();

    if (inputNome) {
      inputNome.focus();
    }
  }

  function inicializar() {
    // Mapeamento dos elementos
    formCartinha = document.getElementById('form-cartinha');
    inputNome = document.getElementById('nome-crianca');
    inputIdade = document.getElementById('idade-crianca');
    inputCidade = document.getElementById('cidade-crianca');
    inputPedidos = document.getElementById('pedidos-crianca');
    radiosComportamento = document.querySelectorAll('input[name="comportamento"]');
    contadorCaracteres = document.getElementById('contador-caracteres');
    erroNome = document.getElementById('erro-nome');
    erroIdade = document.getElementById('erro-idade');
    erroPedidos = document.getElementById('erro-pedidos');
    sucessoValidacao = document.getElementById('sucesso-validacao');

    cartaNome = document.getElementById('carta-nome');
    cartaIdade = document.getElementById('carta-idade');
    cartaCidade = document.getElementById('carta-cidade');
    cartaComportamentoContainer = document.getElementById('carta-comportamento-container');
    cartaPedidos = document.getElementById('carta-pedidos');
    cartaAssinatura = document.getElementById('carta-assinatura');
    cartaData = document.getElementById('carta-data');
    pergaminhoCarta = document.getElementById('pergaminho-carta');

    btnValidar = document.getElementById('btn-validar-cartinha');
    btnLimpar = document.getElementById('btn-limpar-cartinha');
    btnIniciar = document.getElementById('btn-iniciar-cartinha');
    btnConhecerMagia = document.getElementById('btn-conhecer-magia');

    // Data no pergaminho
    if (cartaData) {
      cartaData.textContent = formatarDataNatal();
    }

    // Listeners em tempo real para campos de texto
    if (inputNome) {
      inputNome.addEventListener('input', () => {
        if (inputNome.value.trim()) {
          limparErroGentil(inputNome, erroNome);
        }
        atualizarPergaminhoAoVivo();
      });
    }

    if (inputIdade) {
      inputIdade.addEventListener('input', () => {
        const val = inputIdade.value.trim();
        if (val === '') {
          limparErroGentil(inputIdade, erroIdade);
        } else {
          const num = Number(val);
          if (!isNaN(num) && num >= 1 && num <= 120 && Number.isInteger(num)) {
            limparErroGentil(inputIdade, erroIdade);
          }
        }
        atualizarPergaminhoAoVivo();
      });
    }

    if (inputCidade) {
      inputCidade.addEventListener('input', () => {
        atualizarPergaminhoAoVivo();
      });
    }

    if (inputPedidos) {
      inputPedidos.addEventListener('input', () => {
        const val = inputPedidos.value;
        if (contadorCaracteres) {
          contadorCaracteres.textContent = `${val.length}/1000`;
        }
        if (val.trim()) {
          limparErroGentil(inputPedidos, erroPedidos);
        }
        atualizarPergaminhoAoVivo();
      });
    }

    // Listeners do seletor lúdico de comportamento
    radiosComportamento.forEach((radio) => {
      radio.addEventListener('change', () => {
        atualizarComportamentoNaCarta(radio.value);
      });
    });

    // Submissão e validação do formulário (apenas submit do form para evitar execução duplicada)
    if (formCartinha) {
      formCartinha.addEventListener('submit', validarFormulario);
    }

    // Botão de recomeçar/limpar
    if (btnLimpar) {
      btnLimpar.addEventListener('click', resetarFormulario);
    }

    // Botão de boas-vindas "Escrever Minha Cartinha"
    if (btnIniciar) {
      btnIniciar.addEventListener('click', () => {
        const area = document.getElementById('area-da-cartinha');
        if (area) {
          area.classList.remove('d-none');
          area.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        if (inputNome) {
          inputNome.focus();
        }
      });
    }

    // Botão "A Magia do Natal"
    if (btnConhecerMagia) {
      btnConhecerMagia.addEventListener('click', () => {
        const banner = document.querySelector('.welcome-banner');
        if (banner) {
          banner.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }

    // Inicialização da carta e destaque inicial
    atualizarComportamentoNaCarta(obterComportamentoSelecionado());
    atualizarPergaminhoAoVivo();
  }

  // Inicializa quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializar);
  } else {
    inicializar();
  }
})();
