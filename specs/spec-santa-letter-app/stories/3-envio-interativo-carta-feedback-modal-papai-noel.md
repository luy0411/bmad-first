---
title: 'Envio interativo da carta com feedback festivo e modal do Papai Noel'
type: 'feature'
created: '2026-09-12'
status: 'draft'
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

**Problem:** Depois de escrever a cartinha, a criança precisa vivenciar a emoção de despachá-la para o Polo Norte com um retorno mágico, celebrativo e imediato, sem atrito ou telas frias de confirmação.

**Approach:** Implementar a simulação interativa de envio mágico da carta ao acionar o botão "Enviar ao Papai Noel", disparando efeitos visuais comemorativos na tela e abrindo um modal festivo com uma mensagem calorosa e personalizada do Papai Noel e o selo oficial comemorativo do Polo Norte, atendendo a CAP-3 de forma 100% client-side.

## Boundaries & Constraints

**Always:**
- Utilizar exclusivamente HTML5, CSS3, JavaScript Vanilla e Bootstrap 5 via CDN (sem build steps ou dependências pesadas).
- Arquitetura 100% client-side: simulação de envio e mensagem do Papai Noel geradas e exibidas instantaneamente no navegador, sem backend, APIs externas de IA ou envio SMTP real.
- Acessibilidade e ergonomia infantil: botões e controles com área de toque mínima de 48px x 48px, anéis de foco visíveis (`:focus-visible`), modal acessível com suporte a fechamento por tecla ESC ou botão fechar com área ampla.
- Mensagem acolhedora do Papai Noel personalizada com o nome da criança e alinhada ao comportamento declarado.
- Feedback visual imediato sem recarregar a página.

**Never:**
- Sem envio real de e-mails para servidores externos.
- Sem alertas nativos do navegador (`window.alert`).
- Sem bloqueio do usuário ou recarregamento de página.
- Sem dependências pesadas ou chamadas de rede.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Envio com dados válidos | Carta preenchida e clique em "Enviar ao Papai Noel" | Animação festiva de despacho, abertura do modal com mensagem carinhosa personalizada do Papai Noel e selo do Polo Norte | Sem erro esperado |
| Tentativa de envio com dados incompletos | Clique em "Enviar ao Papai Noel" sem nome ou pedidos | Validação gentil acionada, exibição dos alertas amigáveis e foco no primeiro campo pendente sem abrir modal | Foco suave no campo pendente |
| Fechamento do modal | Clique no botão de fechar, clique fora (backdrop) ou tecla ESC | Modal fecha suavemente e retorna o foco acessível ao botão de envio | Sem erro esperado |
| Reabertura após alteração | Edição do formulário e novo clique em envio | Mensagem do Papai Noel atualizada com os novos dados | Sem erro esperado |

</intent-contract>

## Code Map

- `index.html` -- Inclusão do botão proeminente de envio festivo e da estrutura semântica do Modal do Papai Noel (Bootstrap 5 modal com acessibilidade).
- `css/style.css` -- Estilos do modal festivo natalino, selo postal dourado do Polo Norte, botão de envio comemorativo e animações suaves de despacho.
- `js/app.js` -- Lógica de despacho festivo, validação pré-envio, geração do texto personalizado do Papai Noel e controle do modal.
- `tests/verify_story_3.py` -- Testes automatizados cobrindo disparo do modal, personalização do texto, acessibilidade (área de toque >= 48px, ESC, foco) e ausência de chamadas de rede.

## Tasks & Acceptance

**Execution:**
- [ ] `index.html` -- Adicionar o botão de envio mágico "Enviar ao Papai Noel" e a estrutura semântica do Modal natalino com selo do Polo Norte -- Atende a CAP-3 com interface festiva e acolhedora.
- [ ] `css/style.css` -- Desenvolver estilos do modal temático (fundo translúcido, bordas douradas, tipografia acolhedora e botão de envio destacado) -- Garante atmosfera mágica e ergonomia (min 48px).
- [ ] `js/app.js` -- Implementar o fluxo de envio mágico, validação, montagem da resposta carinhosa do Papai Noel e acionamento do modal Bootstrap -- Assegura resposta instantânea 100% local.
- [ ] `tests/verify_story_3.py` -- Criar e executar a suíte de testes automatizados com Firefox Headless -- Valida critérios de aceitação e conformidade sem regressões.

**Acceptance Criteria:**
- Given a cartinha preenchida com dados válidos, when a criança clica no botão "Enviar ao Papai Noel", then uma animação festiva ocorre e o modal do Papai Noel é exibido sem recarregar a página.
- Given o modal aberto, when visualizado, then uma mensagem personalizada chamando a criança pelo nome, celebrando seu comportamento e exibindo o selo oficial do Polo Norte é apresentada com clareza.
- Given a tentativa de envio com campos essenciais em branco, when o botão de envio é clicado, then o modal não se abre e as validações gentis direcionam a criança aos campos pendentes.
- Given o modal aberto, when a criança ou responsável aciona o botão fechar, o backdrop ou a tecla ESC, then o modal se encerra suavemente mantendo a integridade da aplicação.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

- Estilizar o modal com cabeçalho natalino vermelho e dourado, selo postal comemorativo ("Oficial do Polo Norte") e texto carinhoso assinado pelo "Papai Noel e os Duendes".
- O botão de envio "Enviar ao Papai Noel" deve ter destaque visual supremo (área de toque ampla >= 48px, cores contrastantes e ícone de foguete/trenó natalino 🎅✨).

## Verification

**Commands:**
- `python3 tests/verify_story_3.py` -- expected: Todos os testes de envio mágico, abertura de modal e acessibilidade passam com sucesso.

**Manual checks (if no CLI):**
- Preencher a cartinha, clicar em "Enviar ao Papai Noel", verificar a mensagem personalizada no modal, selo do Polo Norte e fechamento acessível.
