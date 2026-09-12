---
title: 'Estrutura base da SPA com tema natalino e layout responsivo'
type: 'feature'
created: '2026-09-12'
status: 'done'
baseline_commit: 'NO_VCS'
route: 'full'
review_loop_iteration: 0
context:
  - 'specs/spec-santa-letter-app/SPEC.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** A aplicação precisa de uma estrutura web inicial temática e acolhedora, garantindo que crianças e responsáveis em qualquer dispositivo encontrem uma atmosfera natalina agradável e sem barreiras de usabilidade.

**Approach:** Criar a estrutura base HTML5 com Bootstrap 5 via CDN, folha de estilos CSS personalizada com tema natalino (vermelho festivo, verde pinheiro, dourado), efeito sutil de neve decorativa e botões ergonômicos com área de toque mínima de 48px, com layout responsivo para resoluções de 360px a 1920px (CAP-4).

## Boundaries & Constraints

**Always:**
- Utilizar exclusivamente HTML5, CSS3 e Bootstrap 5 via CDN (sem build step, npm, webpack ou frameworks pesados).
- Garantir dimensões mínimas de 48px x 48px para elementos interativos e botões (ergonomia infantil).
- Paleta visual natalina: tons de vermelho festivo, verde pinheiro, dourado e branco neve com alto contraste.
- Responsividade fluida entre 360px (mobile pequeno) e 1920px (desktop full HD).
- Arquitetura 100% estática/client-side direta (abrir `index.html` diretamente no navegador).

**Never:**
- Sem frameworks frontend pesados (React, Vue, Angular).
- Sem dependências de backend, servidor Node.js ou chamadas de API externas.
- Sem anúncios, rastreadores, cookies de terceiros ou telemetria.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Carregamento inicial em desktop (>=992px) | Abertura do `index.html` em tela de 1920x1080 | Layout centralizado acolhedor, tipografia legível, neve animada em segundo plano sem cobrir interações | Sem erro esperado |
| Carregamento em smartphone (360px) | Abertura do `index.html` em tela móvel de 360px | Layout adaptado em coluna única sem scroll horizontal, botões >= 48px | Sem erro esperado |
| Navegador com redução de movimento | Preferência `prefers-reduced-motion: reduce` ativa no sistema operacional | Animação de neve desativada ou pausada para evitar desconforto visual | Sem erro esperado |

</frozen-after-approval>

## Code Map

- `index.html` -- Esqueleto principal da SPA, carregamento do Bootstrap 5 via CDN, container principal com cabeçalho natalino e área estruturada para as próximas histórias.
- `css/style.css` -- Folha de estilos natalina com variáveis CSS para paleta de cores, botões ergonômicos, tipografia e animação suave de flocos de neve.

## Tasks & Acceptance

**Execution:**
- [x] `index.html` -- Criação do esqueleto HTML5 com meta tags responsivas, Bootstrap 5 CDN, container festivo e elementos estruturais básicos -- Estabelece a estrutura inicial da aplicação conforme CAP-4.
- [x] `css/style.css` -- Implementação das regras CSS com tema natalino, variáveis de cores (vermelho/verde/dourado), animação de neve em CSS puro e regras ergonômicas (min 48px) -- Garante atmosfera mágica e usabilidade infantil sem frameworks adicionais.

**Acceptance Criteria:**
- Given que um usuário abre o `index.html` em qualquer navegador moderno, when a página é carregada, then o cabeçalho natalino festivo e o fundo com tema de Natal e neve suave são renderizados imediatamente sem erros no console.
- Given uma tela com largura de 360px a 1920px, when a janela é redimensionada, then o layout se adapta fluidamente sem gerar rolagem horizontal ou sobreposição de elementos.
- Given qualquer elemento de botão ou ação interativa na tela, when inspecionado no navegador, then a área de toque possui no mínimo 48x48px.

## Implementation Notes

- Criada a folha `css/style.css` definindo variáveis CSS globais `:root` (`--cor-natal-vermelho`, `--cor-natal-verde`, `--cor-natal-dourado`, `--cor-neve-fundo`, etc.).
- Desenvolvida animação de queda de neve decorativa em CSS puro com 18 flocos variados e `pointer-events: none` para não interceptar cliques.
- Implementada regra de acessibilidade `@media (prefers-reduced-motion: reduce)` desativando animações quando solicitado pelo sistema operacional.
- Configurada regra ergonômica universal para botões e controles interativos garantindo área de toque mínima de 48px x 48px (altura e largura) com foco visual e estados táteis.
- Estruturado o arquivo `index.html` com Bootstrap 5 via CDN, cabeçalho natalino com selo do Polo Norte, cartão festivo responsivo e área demarcada para as histórias seguintes.
- Validação executada de 360px a 1920px em Firefox Headless sem erros de console ou rolagem horizontal.

## Spec Change Log

## Review Triage Log

- BH-1: low | tests/verify_story_1.py | Caminhos absolutos fixados quebram portabilidade em outros ambientes; roteado para patch.
- BH-2: medium | css/style.css | Remoção de outline sem substituto acessível (:focus-visible) prejudica navegação por teclado; roteado para patch.
- BH-3: low | css/style.css | Seletores globais de botão podem colidir com botões de fechar modais no futuro; roteado para patch.
- BH-4: false | index.html | Lógica JavaScript de envio e formulário pertence explicitamente às Histórias 2 e 3 do projeto, e não à História 1 (layout/estrutura).
- BH-5: low | index.html | Ausência de crossorigin nos links de CDN; roteado para patch.
- BH-6: low | index.html | Falta de meta theme-color e favicon para evitar requisições 404 em navegadores; roteado para patch.
- BH-7: low | index.html | Emojis decorativos sem aria-hidden podem poluir leitura em leitores de tela; roteado para patch.
- BH-8: low | index.html | Ausência de link de pular para conteúdo principal (skip-to-content); roteado para patch.
- BH-9: low | index.html, css/style.css | Glifo de floco de neve pode renderizar como emoji azul no iOS sem seletor de texto \uFE0E; roteado para patch.
- BH-10: low | tests/verify_story_1.py | Uso de porta fixa e escrita de arquivo temporário na raiz do projeto; roteado para patch.
- BH-11: low | css/style.css | Flocos de neve sem will-change: transform podem perder fluidez em dispositivos modestos; roteado para patch.
- BH-12: low | tests/verify_story_1.py | Verificação estática de prefers-reduced-motion em vez de teste no DOM; roteado para patch.
- EC-1: low | tests/verify_story_1.py | Falta de tratamento de erro em JSONDecodeError no handler HTTP de teste; roteado para patch.
- EC-2: low | tests/verify_story_1.py | Caminhos absolutos duplicados (mesmo de BH-1); roteado para patch.
- EC-3: low | tests/verify_story_1.py | Encerramento do servidor HTTP em bloco finally; roteado para patch.
- EC-4: low | tests/verify_story_1.py | Falta de tratamento para ausência de Firefox ou timeout; roteado para patch.
- EC-5: low | css/style.css | Badge do cabeçalho pode estourar se texto não quebrar em telas estreitas; roteado para patch.
- EC-6: medium | css/style.css | Remoção de outline para navegação por teclado (mesmo de BH-2); roteado para patch.
- VG-1: low | tests/verify_story_1.py | Teste de prefers-reduced-motion verifica apenas substring no CSS em vez de regra funcional; roteado para patch.
- VG-2: low | tests/verify_story_1.py | Ausência de asserção explícita no DOM para elementos .snowflake e @keyframes snowfall; roteado para patch.
- VG-3: low | tests/verify_story_1.py | Caminhos absolutos fixados (mesmo de BH-1); roteado para patch.
- VG-4: low | tests/verify_story_1.py | Escrita de capturas de tela diretamente no diretório Downloads; roteado para patch.

## Design Notes

- Usar animação de flocos de neve em CSS puro com `pointer-events: none` e `z-index` adequado para não interceptar cliques.
- Definir variáveis CSS (`:root`) para consistência: `--cor-natal-vermelho`, `--cor-natal-verde`, `--cor-natal-dourado`, `--cor-neve-fundo`.

## Verification

**Manual checks (if no CLI):**
- Abrir `index.html` no navegador e verificar se o tema natalino e estilos são renderizados corretamente.
- Inspecionar elementos no DevTools do navegador em resoluções 360px, 768px e 1920px confirmando responsividade fluida e dimensões mínimas dos botões (48px).
