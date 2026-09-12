# 🎅 Cartinha para o Papai Noel (Santa Letter App)
> **Projeto Prático de Introdução e Estudos com o BMad Method**

Este repositório foi criado como um ambiente prático e didático para **iniciar os estudos com o BMad (BMad Method)** — uma metodologia estruturada de engenharia de software assistida por agentes de inteligência artificial baseada em **Spec-Driven Development** (Desenvolvimento Guiado por Especificações).

---

## 🎯 Objetivo dos Estudos com o BMad

O propósito deste repositório é demonstrar o ciclo de vida completo do desenvolvimento com BMad, desde o contrato de requisitos até o código entregue e verificado:

- **Especificações como Contrato Canônico:** Uso de especificações formais ([`SPEC.md`](specs/spec-santa-letter-app/SPEC.md)) como a única fonte da verdade e contrato de preservação para funcionalidades, restrições e não-objetivos.
- **Divisão em Histórias Atômicas:** Quebra dos requisitos em histórias rastreáveis ([`stories.yaml`](specs/spec-santa-letter-app/stories.yaml) e pastas `stories/`).
- **Papéis Especializados de Agentes:** Orquestração do trabalho através de personas com responsabilidades bem delimitadas (configuradas em [`_bmad/config.toml`](_bmad/config.toml)):
  - 📊 **Mary** (Business Analyst): Análise estratégica e levantamento de evidências.
  - 📋 **John** (Product Manager): Definição de escopo, PRD e foco no valor ao usuário final.
  - 🎨 **Sally** (UX Designer): Experiência do usuário, acessibilidade e ergonomia.
  - 🏗️ **Winston** (System Architect): Arquitetura técnica, decisões de baixo risco e conformidade.
  - 💻 **Amelia** (Senior Software Engineer): Implementação orientada a testes, critérios de aceitação e código limpo.
- **Ciclo de Revisão e Rastreabilidade:** Registro sistemático de revisões, edge cases e logs de triagem antes da conclusão de cada história.

---

## 📖 Sobre o Projeto: Cartinha para o Papai Noel

A aplicação desenvolvida para exercitar o método é uma **Single Page Application (SPA)** festiva, mágica e sem atrito para que crianças (acompanhadas ou não dos pais) possam escrever e enviar sua cartinha de Natal diretamente para o Polo Norte.

### 🌟 Capacidades (do [`SPEC.md`](specs/spec-santa-letter-app/SPEC.md))

- **CAP-1 (Formulário e Redação):** Preenchimento de dados essenciais (nome, idade, cidade e pedidos/mensagem) com tipografia legível, botões grandes e validações gentis sem jargões técnicos.
- **CAP-2 (Seletor Lúdico de Comportamento):** Seleção divertida de como a criança se comportou no ano (ex.: *"Fui muito bonzinho(a)"*, *"Tentei bastante"*, *"Às vezes fiz travessura"*), destacada visualmente e integrada à carta.
- **CAP-3 (Envio Mágico com Celebração):** Simulação mágica de envio instantâneo sem recarregar a página, com animação comemorativa e exibição de modal acolhedor com mensagem do Papai Noel e selo do Polo Norte.
- **CAP-4 (Layout Temático e Responsivo):** Interface festiva (paleta vermelho, verde pinheiro e dourado, neve suave em segundo plano), responsiva de 360px a 1920px e botões ergonômicos para crianças (área de toque $\ge$ 48x48px).
- **CAP-5 (Impressão como Lembrança Física):** Geração de versão limpa para folha de papel via `window.print()`, ocultando controles web e formatando a cartinha como recordação natalina.

### ⚙️ Restrições Técnicas & Arquitetura

- **100% Client-Side:** Toda validação, lógica e resposta ocorrem no navegador do usuário, sem backend, servidor Node.js ou banco de dados.
- **Sem Build Step:** Aplicação desenvolvida em HTML5, CSS3, JavaScript Vanilla e Bootstrap 5 via CDN. Executa diretamente ao abrir o arquivo no navegador.
- **Privacidade Infantil Garantida:** Nenhum dado pessoal é transmitido para a internet, servidores remotos, serviços de analytics ou telemetria.
- **Acessibilidade:** Suporte a `prefers-reduced-motion` (desativação de animações de neve para usuários sensíveis) e foco visível para navegação via teclado.

### 🚫 Não-Objetivos (Non-Goals)

- Sem envio real de e-mails via SMTP ou servidores de terceiros.
- Sem autenticação, criação de contas ou telas de login.
- Sem publicidade, banners, links de afiliados ou monetização.
- Sem persistência remota em nuvem.

---

## 🗺️ Roadmap de Implementação (Histórias)

Conforme planejado em [`specs/spec-santa-letter-app/stories.yaml`](specs/spec-santa-letter-app/stories.yaml):

| História | Título | Status | Descrição |
|---|---|:---:|---|
| **1** | [Estrutura base da SPA com tema natalino](specs/spec-santa-letter-app/stories/1-estrutura-base-tema-natalino-layout-responsivo.md) | ✅ Concluída | Esqueleto HTML5/CSS, Bootstrap 5 CDN, efeito de neve, paleta natalina e layout responsivo de 360px a 1920px (CAP-4). |
| **2** | Formulário de redação da carta e seletor de comportamento | ⏳ Próxima | Campos de dados, validações gentis e seletor lúdico de comportamento (CAP-1 e CAP-2). |
| **3** | Envio interativo da carta e modal do Papai Noel | 📋 Planejada | Simulação de envio com retorno celebrativo, animação e modal festivo (CAP-3). |
| **4** | Impressão estilizada da cartinha física | 📋 Planejada | Regras `@media print` e botão para impressão limpa da cartinha de recordação (CAP-5). |

---

## 🚀 Como Executar o Projeto

Como o projeto foi planejado sob a restrição de **execução sem build step**, não é necessário instalar dependências via `npm` ou configurar servidores complexos.

### Opção 1: Abrir diretamente no navegador
Basta dar um duplo clique no arquivo [`index.html`](index.html) ou abri-lo com qualquer navegador web moderno:
```bash
# No Linux:
xdg-open index.html

# No macOS:
open index.html
```

### Opção 2: Servidor local simples (opcional)
Se preferir rodar com um servidor HTTP local simples:
```bash
python3 -m http.server 8000
```
Em seguida, acesse no navegador: [http://localhost:8000](http://localhost:8000)

---

## 📂 Estrutura de Diretórios

```plaintext
bmad-first/
├── _bmad/                  # Configurações do framework BMad e personas de agentes
│   └── config.toml         # Configuração dos agentes (Mary, John, Sally, Winston, Amelia)
├── css/
│   └── style.css           # Estilos temáticos natalinos, animação de neve e regras de ergonomia
├── specs/                  # Contratos canônicos de especificação BMad
│   └── spec-santa-letter-app/
│       ├── SPEC.md         # Especificação canônica do projeto (regras, CAPs e restrições)
│       ├── stories.yaml    # Lista e estado das histórias de implementação
│       └── stories/        # Detalhamento e critérios de aceitação de cada história
├── index.html              # Página principal da aplicação (SPA)
└── README.md               # Apresentação do projeto e guia de estudos BMad
```

---

## 📚 Como Praticar e Estudar o BMad neste Repositório

1. **Leia a Especificação:** Explore o arquivo [`specs/spec-santa-letter-app/SPEC.md`](specs/spec-santa-letter-app/SPEC.md) para entender como uma SPEC canônica deve ser formulada (Porquê, Capacidades, Restrições, Não-objetivos).
2. **Acompanhe a Execução de Histórias:** Veja em [`specs/spec-santa-letter-app/stories/1-estrutura-base-tema-natalino-layout-responsivo.md`](specs/spec-santa-letter-app/stories/1-estrutura-base-tema-natalino-layout-responsivo.md) como critérios de aceitação, mapeamento de código e triagem de revisão são documentados.
3. **Avance no Desenvolvimento:** Utilize os agentes BMad (como o agente Dev Amelia) para implementar a História 2 e dar continuidade ao fluxo de desenvolvimento orientado a especificações.
