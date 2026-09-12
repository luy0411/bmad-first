---
id: SPEC-santa-letter-app
companions: []
sources: []
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate.

# Cartinha para o Papai Noel (Santa Letter App)

## Porquê (Why)

Na época natalina, as crianças sonham em compartilhar seus desejos, histórias e pedidos com o Papai Noel. No entanto, o envio de cartas físicas pode ser demorado ou inacessível, enquanto formulários digitais convencionais costumam ser frios, complexos ou repletos de cadastros e anúncios. Este projeto cria uma experiência digital festiva, mágica e sem atrito, onde crianças (sozinhas ou acompanhadas dos pais) podem escrever sua cartinha de Natal em uma página temática e colorida, declarar seu comportamento no ano e vivenciar a alegria de enviar sua mensagem direto para o Polo Norte com um retorno visual acolhedor e encantador.

## Capacidades (Capabilities)

- **CAP-1**
  - **intent:** A criança pode preencher seus dados básicos (nome, idade, cidade) e redigir seus pedidos e mensagens para o Papai Noel em campos claros, com tipografia legível e botões grandes.
  - **success:** A interface valida campos essenciais (como nome e mensagem) com avisos visuais gentis e sem jargões técnicos.

- **CAP-2**
  - **intent:** A criança pode escolher de forma lúdica como se comportou durante o ano (ex: "Fui muito bonzinho(a)", "Tentei bastante", "Às vezes fiz travessura").
  - **success:** O estado selecionado é destacado visualmente com ícones natalinos e integrado ao corpo final da carta.

- **CAP-3**
  - **intent:** A criança pode acionar o envio da carta e receber uma celebração mágica imediata na tela, confirmando o recebimento no Polo Norte.
  - **success:** O clique em "Enviar ao Papai Noel" dispara uma animação festiva e exibe uma mensagem calorosa de resposta do Papai Noel em um modal ou painel comemorativo, sem recarregar a página.

- **CAP-4**
  - **intent:** A criança e seus responsáveis visualizam a aplicação de forma adaptada tanto em celulares/tablets quanto em computadores, com atmosfera natalina (paleta vermelho/verde/dourado, neve suave, ilustrações amigáveis).
  - **success:** A página se reconfigura fluidamente via Bootstrap 5 em telas de 360px a 1920px, mantendo botões fáceis de tocar e sem quebras de layout.

- **CAP-5**
  - **intent:** Os pais ou a criança podem imprimir ou gerar uma versão limpa da cartinha preenchida como lembrança física de Natal.
  - **success:** O acionamento de um botão "Imprimir / Guardar" dispara a impressão do navegador (`window.print()`) com folha estilizada sem elementos da interface web (menu e botões ocultos na impressão).

## Restrições (Constraints)

- **Stack Tecnológica Estrita:** Single Page Application (SPA) construída exclusivamente com HTML5, CSS3, JavaScript Vanilla e Bootstrap 5 (via CDN).
- **Arquitetura 100% Client-Side:** Toda a lógica de envio, validação e resposta é processada localmente no navegador, sem backend, servidor ou banco de dados.
- **Privacidade e Proteção de Dados Infantis:** Nenhum dado pessoal da criança ou conteúdo da carta é transmitido para a nuvem, servidores externos ou ferramentas de telemetria.
- **Execução Sem Build Step:** O projeto é executável diretamente abrindo o arquivo `index.html` em qualquer navegador web moderno.
- **Design Ergonômico Infantil:** Elementos clicáveis possuem área mínima de toque de 48x48px, contraste de cores acessível e linguagem visual intuitiva.

## Não-Objetivos (Non-goals)

- Sem envio real de e-mails via SMTP ou servidores de correio eletrônico externos.
- Sem sistema de autenticação, login, senhas ou cadastro de contas de usuários.
- Sem anúncios publicitários, monetização ou links de comércio eletrônico.
- Sem sincronização de dados em nuvem entre dispositivos.
- Sem integração com APIs externas de IA em tempo real para respostas dinâmicas.

## Sinal de Sucesso (Success signal)

Uma criança (ou responsável) consegue abrir a página em qualquer navegador moderno (desktop ou smartphone), preencher seu nome, idade e desejos, escolher sua classificação de comportamento e acionar o botão de envio em menos de 2 minutos — recebendo imediatamente na tela a celebração visual com selo do Polo Norte e mensagem carinhosa de confirmação do Papai Noel, além de poder acionar a impressão física limpa da cartinha estilizada sem erros ou recarregamento da página.
