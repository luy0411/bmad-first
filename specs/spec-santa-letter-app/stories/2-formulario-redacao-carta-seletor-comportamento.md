---
title: 'Formulário de redação da carta e seletor lúdico de comportamento'
type: 'feature'
created: '2026-09-12'
status: 'done'
baseline_revision: '6511cbd000d7dbffc80d41df444e467627ac9163'
route: 'full'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - 'specs/spec-santa-letter-app/SPEC.md'
warnings: []
deferred: []
---

<intent-contract>

## Intent

**Problem:** Para que a experiência mágica aconteça, as crianças e famílias precisam de uma forma amigável, acolhedora e acessível de redigir a cartinha, informando quem são, seus pedidos e como se comportaram no ano, sem enfrentar formulários técnicos frios ou alertas intrusivos.

**Approach:** Implementar a interface de redação com campos semânticos para nome, idade, cidade e pedidos, combinada a um seletor visual lúdico de comportamento com ícones natalinos e feedback gentil integrado ao pergaminho da carta, atendendo a CAP-1 e CAP-2.

## Boundaries & Constraints

**Always:**
- Utilizar exclusivamente HTML5, CSS3, JavaScript Vanilla e Bootstrap 5 via CDN (sem build step, npm ou dependências pesadas).
- Arquitetura 100% client-side: todas as validações e atualizações da cartinha ocorrem localmente no navegador, sem chamadas a servidores externos ou telemetria.
- Ergonomia e acessibilidade infantil: todas as opções de comportamento e botões interativos devem ter área de toque mínima de 48px x 48px com anel de foco visível.
- Validação gentil e acolhedora: mensagens visuais sem jargões técnicos (ex: "O Papai Noel precisa saber o seu nome para responder!").
- Integração da escolha de comportamento diretamente no corpo do texto da carta de forma natural e festiva.

**Never:**
- Sem requisições de rede, APIs de terceiros ou armazenamento em servidores remotos.
- Sem alertas intrusivos nativos do navegador (`alert()`, `confirm()`).
- Sem frameworks pesados (React, Vue, Angular).
- Sem campos desnecessários de dados sensíveis ou requisitos de login/senha.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Preenchimento completo e válido | Nome, idade, cidade, pedidos e opção de comportamento preenchidos | Carta montada no pergaminho com todos os dados e comportamento integrado | Sem erro esperado |
| Campo de nome ou pedidos vazio ao validar | Clique no botão de confirmação com campos vazios | Mensagens visuais gentis e acolhedoras exibidas próximo aos campos, sem alertas nativos | Foco suave no primeiro campo com pendência |
| Seleção de comportamento | Clique em uma das opções lúdicas de comportamento | Destaque visual no botão/card e atualização imediata do trecho da cartinha | Sem erro esperado |
| Idade não numérica ou menor que 1 | Valor inválido no campo de idade | Ajuste gentil ou mensagem amigável solicitando idade válida | Feedback visual acolhedor |

</intent-contract>

## Code Map

- `index.html` -- Desbloqueio e marcação semântica do formulário de cartinha, seletor de comportamento com cards acessíveis (min 48px), prévia da cartinha e vinculação do script JS.
- `css/style.css` -- Estilos dos inputs natalinos, cards seletores de comportamento com estados de foco e seleção, mensagens de validação gentis e pergaminho da cartinha.
- `js/app.js` -- Lógica client-side para validação acolhedora, sincronização do seletor de comportamento e atualização da cartinha.
- `tests/verify_story_2.py` -- Testes automatizados verificando conformidade de campos, interações, validação gentil e responsividade.

## Tasks & Acceptance

**Execution:**
- [x] `index.html` -- Estruturação do formulário de cartinha e cards do seletor de comportamento dentro de `#area-da-cartinha` -- Provê a interface de entrada acessível para CAP-1 e CAP-2.
- [x] `css/style.css` -- Adição dos estilos festivos para inputs, botões do seletor de comportamento (min 48px) e mensagens de validação -- Garante atmosfera mágica e usabilidade infantil ergonômica.
- [x] `js/app.js` -- Implementação das validações amigáveis e montagem em tempo real da cartinha no pergaminho -- Assegura fluxo lúdico sem requisições externas.
- [x] `tests/verify_story_2.py` -- Criação e execução da suíte de verificação automatizada -- Garante cobertura dos critérios de aceitação e estabilidade.

**Acceptance Criteria:**
- Given a página carregada com o formulário aberto, when a criança visualiza a tela, then campos para nome, idade, cidade, pedidos e opções lúdicas de comportamento estão visíveis e utilizáveis.
- Given o seletor de comportamento, when a criança clica em qualquer opção ("Fui muito bonzinho(a)", "Tentei bastante", "Às vezes fiz travessura"), then a opção recebe destaque visual com ícone natalino e área de toque >= 48px, refletindo o texto na cartinha.
- Given a tentativa de avançar com nome ou pedidos não preenchidos, when a validação é acionada, then mensagens acolhedoras e sem jargões técnicos são exibidas visualmente sem uso de alerts nativos.
- Given todos os dados preenchidos corretamente, when validados, then a cartinha final reflete nome, idade, cidade, comportamento e pedidos sem recarregar a página ou disparar requisições externas.

## Implementation Notes

- `#area-da-cartinha` desbloqueada no `index.html` com layout de 2 colunas no desktop (formulário acessível à esquerda e pergaminho interativo à direita) e empilhamento fluido no mobile.
- `js/app.js` implementado com arquitetura 100% client-side, sem chamadas externas, sem dependências e sem alertas intrusivos (`alert()`, `confirm()`).
- Seletor lúdico de comportamento criado com 3 opções temáticas (`"Fui muito bonzinho(a)"`, `"Tentei bastante"`, `"Às vezes fiz travessura"`) com ícones natalinos (`😇`, `⭐`, `🍪`), áreas de toque superiores a 48px x 48px e `:focus-visible` de alto contraste.
- Validação gentil em tempo real com mensagens acolhedoras exibidas inline e direcionamento suave de foco para campos pendentes.
- Sincronização viva no pergaminho que atualiza dinamicamente nome, idade, cidade, texto festivo do comportamento e mensagem de pedidos.
- Suíte `tests/verify_story_2.py` validando estática e dinamicamente no Firefox Headless (360px, 768px e 1920px), com zero erros de console e sem rolagem horizontal.

## Spec Change Log

## Review Triage Log

### 2026-09-12 — Review pass
- verdicts: 19 findings — high 0, medium 0, low 16, false 3, maybe-false 0
- findings:
  - `[low]` `[patch]` Duplicate Form Submission Handlers — Removido addEventListener de clique de btnValidar; submit tratado exclusivamente por formCartinha.
  - `[low]` `[patch]` Missing Upper Bound and Float Validation for Age — Validação atualizada para rejeitar idades negativas, decimais ou maiores que 120.
  - `[low]` `[patch]` Grammar Mismatch in Parchment Age Expression ("1 anos") — Ajustada concordância no pergaminho para "1 ano" no singular e "X anos" no plural.
  - `[low]` `[patch]` Unhandled Optional Age in Letter Preview — Omissão fluida da cláusula de idade quando o campo não estiver preenchido.
  - `[low]` `[patch]` Orphaned City Error Element in DOM — Removidos o container #erro-cidade e o atributo aria-describedby="erro-cidade".
  - `[false]` `[reject]` Unprotected Destructive Form Reset ("Recomeçar") — O reset direto de formulário sem alertas bloqueantes atende à diretriz de ausência de atrito e zero alertas intrusivos.
  - `[low]` `[patch]` Conflicting ARIA Grouping Roles on Behavior Radiogroup — Removidos role="radiogroup" e aria-label da div interna, mantendo a semântica nativa de fieldset/legend.
  - `[false]` `[reject]` Missing Character Limit Warning State — O contador dinâmico X/1000 já fornece feedback visual em tempo real e o maxlength impede extrapolação.
  - `[low]` `[patch]` Missing Screen-Reader and Keyboard Focus Shift on Validation Success — Adicionado foco programático em pergaminhoCarta.focus() após validação com sucesso.
  - `[false]` `[reject]` Dead-End Workflow Post-Validation — O avanço de envio e impressão pertence explicitamente ao escopo das Histórias 3 e 4.
  - `[low]` `[patch]` Gaps in Verification Test Coverage — Adicionadas asserções automatizadas em tests/verify_story_2.py cobrindo reset, idade estrita e foco.
  - `[low]` `[patch]` Invalid non-numeric input or excessive ages bypass validation — Mesma causa raiz de verificação de idade; corrigido em js/app.js.
  - `[low]` `[patch]` Premature Timeout Clear on Repeated Submissions — Adicionado clearTimeout(timerDestaquePergaminho) antes de agendar nova animação.
  - `[low]` `[patch]` Form reset and restart functionality ('Recomeçar') has no test coverage — Adicionado teste automatizado clicando em #btn-limpar-cartinha e validando restauração do estado inicial.
  - `[low]` `[patch]` Real-time typing synchronization on the parchment is masked by form validation submission — Adicionada asserção verificando sincronização do pergaminho antes do submit.
  - `[low]` `[patch]` Real-time dismissal of validation errors on input is masked by submission error clearing — Adicionada asserção verificando limpeza imediata da classe is-invalid ao digitar.
  - `[low]` `[patch]` Handwritten signature on the parchment ('carta-assinatura') is never verified — Adicionada asserção verificando o texto de #carta-assinatura.
  - `[low]` `[patch]` Dynamic character counter feedback has no test coverage — Adicionada asserção conferindo o valor do contador ao digitar pedidos.
  - `[low]` `[patch]` Unreferenced error container #erro-cidade and upper bound age check — Agrupado com a limpeza de nós ARIA e validação de idade.

## Design Notes

- Usar inputs estilizados com bordas arredondadas e sombras suaves, com tamanho de fonte de pelo menos 16px para garantir legibilidade e ergonomia.
- Para o seletor de comportamento, utilizar inputs do tipo radio estilizados como cards/botões festivos com ícones (😇, ⭐, 🍪) e dimensões generosas (mínimo 48px).

## Verification

**Commands:**
- `python3 tests/verify_story_2.py` -- expected: Todos os testes de validação do formulário, seletor de comportamento e acessibilidade passam com sucesso.

**Manual checks (if no CLI):**
- Abrir `index.html` no navegador, preencher o formulário, alternar opções de comportamento e verificar a prévia da cartinha e mensagens visuais gentis.

## Auto Run Result

Status: done

### Summary of implemented change
Implementação completa da História 2 (CAP-1 e CAP-2): formulário semântico e responsivo de redação da cartinha para o Papai Noel com campos para nome, idade, cidade e pedidos, aliado a um seletor lúdico de comportamento com três opções natalinas ("Fui muito bonzinho(a)" 😇, "Tentei bastante" ⭐, "Às vezes fiz travessura" 🍪) e dimensões ergonômicas infantis (>= 48px x 48px). Validações gentis sem jargões técnicos ou alertas nativos (`alert()`, `confirm()`), com espelhamento ao vivo no pergaminho decorativo, assinatura temática e foco acessível.

### Files changed
- `index.html` — Estruturação semântica de `#area-da-cartinha` com formulário `#form-cartinha`, seletor de comportamento e pergaminho interativo.
- `css/style.css` — Estilização natalina dos inputs, cards táteis de comportamento (>= 48px x 48px), mensagens acolhedoras e pergaminho.
- `js/app.js` — Lógica 100% client-side para validação acolhedora, sincronização em tempo real e montagem da cartinha sem recarregar a página.
- `tests/verify_story_2.py` — Suíte de testes automatizados completa com Firefox Headless em 360px, 768px e 1920px.
- `specs/spec-santa-letter-app/stories/2-formulario-redacao-carta-seletor-comportamento.md` — Especificação, log de triage e resultado da execução.

### Review findings breakdown
- Patches aplicados: 16 apontamentos de severidade baixa (handlers duplicados, validação estrita de idade, concordância gramatical, omissão de idade opcional, limpeza de nós ARIA, timeout do pergaminho, foco acessível e cobertura completa de testes em `verify_story_2.py`).
- Itens diferidos: 0
- Apontamentos rejeitados: 3 (reset direto sem diálogo intrusivo, avisos extras de limite de caracteres e botões de fluxo das Histórias 3/4).

### Follow-up review recommendation
`false` — Todas as correções foram pontuais de severidade baixa, sem itens médios ou altos, com 100% dos testes passando sem regressões.

### Verification performed
- `python3 tests/verify_story_2.py` — 100% de sucesso em 360px, 768px e 1920px (cards >= 48px, validação gentil, concordância gramatical, foco acessível, reset e tempo real).
- `python3 tests/verify_story_1.py` — 100% de sucesso (garantia de não-regressão na base natalina, flocos de neve e acessibilidade).

### Residual risks
Nenhum risco residual detectado. Aplicação opera 100% no navegador sem persistência remota e pronta para acoplar a animação de envio e modal da História 3 (CAP-3).
