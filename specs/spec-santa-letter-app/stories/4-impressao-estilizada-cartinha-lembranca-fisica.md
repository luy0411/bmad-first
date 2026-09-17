---
title: 'Impressão estilizada da cartinha como lembrança física'
type: 'feature'
created: '2026-09-16'
status: 'done'
baseline_revision: '796ab8aaf965bdab1ca7195b9f5cceb1c9debe62'
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

**Problem:** Pais e crianças desejam guardar uma recordação física tangível da cartinha enviada ao Papai Noel ou colocá-la sob a árvore de Natal, mas a impressão padrão de páginas web inclui menus, botões funcionais, rodapés e formulários vazios, desperdiçando tinta e estragando a magia natalina.

**Approach:** Implementar suporte completo a impressão estilizada via `@media print` e botões temáticos ergonômicos ("Imprimir / Guardar Lembrança") no formulário e no modal comemorativo. Ao acionar o botão ou invocar a impressão do navegador (`window.print()`), toda a interface funcional (formulários, modais, cabeçalhos, animação de neve e botões) é ocultada, exibindo exclusivamente a cartinha formatada em pergaminho festivo limpo, de alta legibilidade e econômico para impressão doméstica, atendendo a CAP-5 de SPEC.md.

## Boundaries & Constraints

**Always:**
- Utilizar exclusivamente HTML5, CSS3, JavaScript Vanilla e Bootstrap 5 via CDN (sem build steps ou dependências pesadas).
- Arquitetura 100% client-side com acionamento nativo via `window.print()`.
- Ocultar todos os controles interativos no `@media print`: navbar/cabeçalho, coluna do formulário, botões, modais/backdrops, animação de neve e rodapé da página web.
- Exibir e formatar a cartinha (`#pergaminho-carta`) em largura total, fundo claro/limpo econômico, bordas decorativas nítidas e tipografia escura de fácil leitura.
- Prevenir quebras de página impróprias (`page-break-inside: avoid; break-inside: avoid;`).
- Botões de impressão interativos com área de toque mínima de 48px x 48px e foco acessível (`:focus-visible`).

**Never:**
- Sem recarregar a página ou navegar para outra URL.
- Sem bibliotecas externas pesadas para conversão de PDF (usar capacidade nativa de impressão do navegador).
- Sem requisições a servidores remotos ou coleta de dados.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Clique no botão de impressão | Cartinha preenchida e clique em "Imprimir / Guardar Lembrança" | `window.print()` é disparado e folha é formatada exclusivamente com o pergaminho limpo | Sem erro |
| Impressão a partir do modal do Papai Noel | Modal aberto após envio e clique em "Imprimir Lembrança" | Modal e backdrop são ocultados na impressão e folha física destaca a cartinha | Sem erro |
| Disparo de impressão via atalho do navegador (Ctrl+P / Cmd+P) | Usuário aciona atalho nativo do navegador | Regras `@media print` são aplicadas de forma consistente sem botões ou menus | Sem erro |
| Dispositivo móvel com viewport reduzido (360px) | Tela pequena de celular | Botão de impressão com dimensão mínima de 48px e sem quebra ou overflow | Sem overflow |

</intent-contract>

## Code Map

- `index.html` -- Adição do botão "Imprimir / Guardar" (`#btn-imprimir-cartinha`) no grupo de ações do formulário e botão de impressão complementar (`#btn-imprimir-modal`) no rodapé do modal do Papai Noel.
- `css/style.css` -- Inclusão das regras `@media print` estruturadas para ocultar elementos funcionais web (`.festive-header`, `.form-col`, `.festive-footer`, `.modal`, `.modal-backdrop`, `#snow-container`, botões) e estilizar `#pergaminho-carta` como lembrança festiva nítida em folha A4. Estilização do botão `.btn-imprimir-natal` (mínimo 48px).
- `js/app.js` -- Adição dos event listeners para `#btn-imprimir-cartinha` e `#btn-imprimir-modal` disparando `window.print()`.
- `tests/verify_story_4.py` -- Suíte de testes automatizados com Firefox Headless verificando `@media print`, visibilidade do pergaminho, ocultação de controles, ergonomia dos botões (>= 48px) e disparo do método de impressão.

## Tasks & Acceptance

**Execution:**
- [x] `index.html` -- Inserir botões temáticos de impressão com áreas de toque >= 48px -- Atende a CAP-5.
- [x] `css/style.css` -- Desenvolver regras `@media print` e estilos do botão temático -- Garante folha física limpa e econômica.
- [x] `js/app.js` -- Vincular botões ao `window.print()` com tratamento limpo -- Permite impressão imediata.
- [x] `tests/verify_story_4.py` -- Criar e rodar testes de verificação automatizados -- Garante critérios de aceitação.

**Acceptance Criteria:**
- Given a página da aplicação aberta ou o modal exibido, when a criança ou responsável clica no botão de imprimir, then o diálogo nativo `window.print()` é acionado.
- Given o modo de impressão `@media print`, when a visualização de impressão é renderizada, then todos os formulários, botões, modais, navegação e rodapés ficam ocultos (`display: none !important`).
- Given o modo de impressão `@media print`, when a folha é gerada, then apenas a cartinha formatada em pergaminho é impressa com fundo limpo, borda nítida e sem quebra inadequada de página.
- Given qualquer tamanho de tela (360px a 1920px), when os botões de impressão são exibidos, then possuem área de toque superior ou igual a 48px x 48px.

## Implementation Notes

- Adicionado botão temático de impressão `#btn-imprimir-cartinha` no grupo de ações da cartinha e `#btn-imprimir-modal` no rodapé do modal do Papai Noel, ambos com classe `.btn-imprimir-natal` e área de toque superior a 48px x 48px.
- Implementadas regras completas em `@media print` no [`css/style.css`](css/style.css) ocultando formulários, modais, navegação, neve e botões, formatando o pergaminho `#pergaminho-carta` com fundo claro econômico, borda dupla natalina decorativa e `page-break-inside: avoid`.
- Configurado o disparador de impressão em [`js/app.js`](js/app.js) com suporte a cancelamento de evento padrão e acionamento síncrono de `window.print()`.
- Criada e validada a suíte automatizada `tests/verify_story_4.py` cobrindo static checks e testes dinâmicos com Firefox Headless em 360px, 768px e 1920px. Todas as suítes (Histórias 1, 2, 3 e 4) passam com 100% de sucesso.

