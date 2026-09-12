#!/usr/bin/env python3
"""
Testes automatizados dos critérios de aceitação da História 2:
- Estruturação semântica do formulário de cartinha (#area-da-cartinha, #form-cartinha)
- Campos para nome, idade, cidade e pedidos/mensagem
- Seletor lúdico de comportamento com 3 opções ("Fui muito bonzinho(a)", "Tentei bastante", "Às vezes fiz travessura")
- Ícones natalinos (😇, ⭐, 🍪) e dimensões ergonômicas (>= 48px x 48px)
- Validações gentis e acolhedoras sem jargões técnicos e sem alerts nativos
- Foco automático no primeiro campo inválido
- Limpeza imediata de erros ao digitar valores válidos
- Sincronização em tempo real do pergaminho antes e depois do submit
- Assinatura manuscrita temática (#carta-assinatura)
- Contador dinâmico de caracteres (#contador-caracteres)
- Validação estrita de idade (>= 1, <= 120 e inteira) com concordância gramatical ("1 ano" vs "X anos" ou omissão se vazia)
- Transferência de foco acessível para o pergaminho após validação bem-sucedida
- Botão "Recomeçar" (#btn-limpar-cartinha) restaurando estado inicial limpo e foco
- Zero requisições externas, zero dependências pesadas, zero erros de console
- Responsividade fluida (360px, 768px, 1920px) sem overflow horizontal
"""

import http.server
import socketserver
import threading
import subprocess
import urllib.parse
import json
import time
import socket
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = TESTS_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

INDEX_HTML_PATH = BASE_DIR / "index.html"
CSS_STYLE_PATH = BASE_DIR / "css" / "style.css"
JS_APP_PATH = BASE_DIR / "js" / "app.js"

received_reports = []

class AuditHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/report_s2'):
            q = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(q)
            if 'd' in params:
                data = json.loads(params['d'][0])
                received_reports.append(data)
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            self.wfile.write(b'GIF89a')
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def start_server(port):
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(('127.0.0.1', port), AuditHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def main():
    print("=================================================================")
    print(" INICIANDO VERIFICAÇÃO AUTOMATIZADA - HISTÓRIA 2 (REVISÃO REFINADA)")
    print("=================================================================")

    # -------------------------------------------------------------
    # 1. Verificações Estáticas de Arquivos e Código Fonte
    # -------------------------------------------------------------
    print("\n[1/3] Verificando conformidade estática de arquivos e código...")

    if not JS_APP_PATH.exists():
        print(f"  ✗ ERRO: Arquivo {JS_APP_PATH} não encontrado!")
        sys.exit(1)
    print("  ✓ Arquivo js/app.js criado e acessível.")

    with open(JS_APP_PATH, "r", encoding="utf-8") as f:
        js_code = f.read()

    # Verificar proibições (Never: alert(), confirm(), fetch, XMLHttpRequest, frameworks)
    if "alert(" in js_code:
        print("  ✗ ERRO: Uso de alert() detectado no js/app.js!")
        sys.exit(1)
    if "confirm(" in js_code:
        print("  ✗ ERRO: Uso de confirm() detectado no js/app.js!")
        sys.exit(1)
    if "fetch(" in js_code or "XMLHttpRequest" in js_code:
        print("  ✗ ERRO: Requisições de rede detectadas no js/app.js!")
        sys.exit(1)
    print("  ✓ Sem alert(), confirm() ou chamadas de rede externas no js/app.js.")

    # Verificar ausência de listener duplo de clique no btnValidar
    if "btnValidar.addEventListener('click'" in js_code:
        print("  ✗ ERRO: btnValidar ainda possui listener de clique paralelo ao submit!")
        sys.exit(1)
    print("  ✓ Sem listener duplo de clique em btnValidar (apenas handler de submit do form).")

    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html_code = f.read()

    # Verificar marcação semântica em index.html
    required_elements = [
        ('id="form-cartinha"', 'Formulário #form-cartinha'),
        ('id="nome-crianca"', 'Input de nome #nome-crianca'),
        ('id="idade-crianca"', 'Input de idade #idade-crianca'),
        ('id="cidade-crianca"', 'Input de cidade #cidade-crianca'),
        ('id="pedidos-crianca"', 'Textarea de pedidos #pedidos-crianca'),
        ('name="comportamento"', 'Seletor de comportamento'),
        ('id="pergaminho-carta"', 'Pergaminho da carta #pergaminho-carta'),
        ('id="carta-nome"', 'Campo do nome na carta #carta-nome'),
        ('id="carta-comportamento"', 'Campo do comportamento na carta #carta-comportamento'),
        ('id="carta-pedidos"', 'Campo dos pedidos na carta #carta-pedidos'),
        ('id="carta-assinatura"', 'Assinatura na carta #carta-assinatura'),
        ('id="contador-caracteres"', 'Contador de caracteres #contador-caracteres'),
        ('id="btn-validar-cartinha"', 'Botão de validação #btn-validar-cartinha'),
        ('id="btn-limpar-cartinha"', 'Botão de recomeçar #btn-limpar-cartinha'),
        ('<script src="js/app.js"></script>', 'Vinculação do script js/app.js')
    ]
    for pattern, desc in required_elements:
        if pattern in html_code:
            print(f"  ✓ {desc} presente no index.html.")
        else:
            print(f"  ✗ ERRO: {desc} ({pattern}) ausente no index.html!")
            sys.exit(1)

    # Verificar ausência de nó ARIA morto erro-cidade
    if 'id="erro-cidade"' in html_code or 'aria-describedby="erro-cidade"' in html_code:
        print("  ✗ ERRO: Elemento órfão #erro-cidade ou aria-describedby ainda presente no HTML!")
        sys.exit(1)
    print("  ✓ Sem nós ARIA órfãos para cidade.")

    # Verificar remoção do role redundante no fieldset
    if 'role="radiogroup"' in html_code:
        print("  ✗ ERRO: role=\"radiogroup\" redundante ainda presente dentro de fieldset!")
        sys.exit(1)
    print("  ✓ fieldset/legend com semântica nativa limpa sem role redundante.")

    # Verificar opções lúdicas de comportamento no HTML
    required_behaviors = [
        "Fui muito bonzinho(a)",
        "Tentei bastante",
        "Às vezes fiz travessura"
    ]
    for b in required_behaviors:
        if b in html_code:
            print(f"  ✓ Opção de comportamento '{b}' presente no HTML.")
        else:
            print(f"  ✗ ERRO: Opção '{b}' não encontrada no HTML!")
            sys.exit(1)

    required_icons = ["😇", "⭐", "🍪"]
    for ic in required_icons:
        if ic in html_code:
            print(f"  ✓ Ícone festivo '{ic}' presente no HTML.")
        else:
            print(f"  ✗ ERRO: Ícone '{ic}' não encontrado no HTML!")
            sys.exit(1)

    # Verificar estilos CSS
    with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
        css_code = f.read()

    required_css_tokens = [
        ".card-comportamento-inner",
        ".mensagem-ajuda-gentil",
        ".pergaminho-conteudo",
        ".form-control-natal"
    ]
    for token in required_css_tokens:
        if token in css_code:
            print(f"  ✓ Classe CSS '{token}' presente no style.css.")
        else:
            print(f"  ✗ ERRO: Classe CSS '{token}' ausente no style.css!")
            sys.exit(1)

    # -------------------------------------------------------------
    # 2. Inicialização do Servidor HTTP Local para Teste no Browser
    # -------------------------------------------------------------
    port = get_free_port()
    server = start_server(port)
    time.sleep(0.4)

    test_file_path = BASE_DIR / "test_runner_s2.html"

    # Script de auditoria dinâmica em tempo real dentro do navegador
    audit_s2_code = """
    <script>
    window.__pageErrors = [];
    window.__alertIntercepted = false;
    window.__confirmIntercepted = false;

    window.addEventListener('error', (e) => {
        window.__pageErrors.push(e.message);
    });

    window.alert = function() { window.__alertIntercepted = true; };
    window.confirm = function() { window.__confirmIntercepted = true; return true; };

    document.addEventListener('DOMContentLoaded', () => {
        const testResults = {
            cardDimensionsMeets48px: true,
            cardsAudited: [],
            emptyValidationTested: false,
            emptyValidationPassed: false,
            firstErrorFocused: false,
            errorClearOnInputTested: false,
            errorClearOnInputPassed: false,
            realtimeSyncBeforeSubmitTested: false,
            realtimeSyncBeforeSubmitPassed: false,
            charCounterTested: false,
            charCounterPassed: false,
            invalidAgeTested: false,
            invalidAgePassed: false,
            ageGrammarTested: false,
            ageGrammarPassed: false,
            behaviorToggleTested: false,
            behaviorTogglePassed: false,
            fullValidSubmissionTested: false,
            fullValidSubmissionPassed: false,
            letterReflectsAllData: false,
            handwrittenSignaturePassed: false,
            pergaminhoFocusedOnSuccess: false,
            resetButtonTested: false,
            resetButtonPassed: false,
            alertsUsed: false,
            errors: []
        };

        try {
            // 1. Auditoria de Dimensões dos Cards de Comportamento (mínimo 48px x 48px)
            const cards = Array.from(document.querySelectorAll('.card-comportamento-inner'));
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const meets = (rect.width >= 48) && (rect.height >= 48);
                testResults.cardsAudited.push({
                    text: card.textContent.replace(/\\s+/g, ' ').trim(),
                    width: rect.width,
                    height: rect.height,
                    meets48px: meets
                });
                if (!meets) {
                    testResults.cardDimensionsMeets48px = false;
                }
            });

            const inputNome = document.getElementById('nome-crianca');
            const inputIdade = document.getElementById('idade-crianca');
            const inputCidade = document.getElementById('cidade-crianca');
            const inputPedidos = document.getElementById('pedidos-crianca');
            const btnValidar = document.getElementById('btn-validar-cartinha');
            const btnLimpar = document.getElementById('btn-limpar-cartinha');
            const formCartinha = document.getElementById('form-cartinha');
            const contadorCaracteres = document.getElementById('contador-caracteres');
            const erroNome = document.getElementById('erro-nome');
            const erroIdade = document.getElementById('erro-idade');
            const erroPedidos = document.getElementById('erro-pedidos');
            const cartaAssinatura = document.getElementById('carta-assinatura');
            const cartaComportamentoCont = document.getElementById('carta-comportamento-container');
            const cartaPedidos = document.getElementById('carta-pedidos');
            const pergaminhoCarta = document.getElementById('pergaminho-carta');
            const paragrafoApresentacao = document.querySelector('.carta-paragrafo-apresentacao');

            // 2. Teste de Sincronização em Tempo Real Antes do Submit e Contador de Caracteres
            testResults.realtimeSyncBeforeSubmitTested = true;
            inputNome.value = 'Clara';
            inputNome.dispatchEvent(new Event('input'));

            const nomeSyncAntes = document.getElementById('carta-nome').textContent.includes('Clara');
            const assinaturaSyncAntes = cartaAssinatura.textContent.includes('Clara');

            inputPedidos.value = 'Quero um patinete'; // 17 caracteres
            inputPedidos.dispatchEvent(new Event('input'));
            const pedidosSyncAntes = cartaPedidos.textContent.includes('Quero um patinete');

            testResults.charCounterTested = true;
            testResults.charCounterPassed = (contadorCaracteres.textContent === '17/1000');
            testResults.realtimeSyncBeforeSubmitPassed = nomeSyncAntes && assinaturaSyncAntes && pedidosSyncAntes;

            // 3. Teste de Validação Vazia e Foco Inicial
            testResults.emptyValidationTested = true;
            inputNome.value = '';
            inputPedidos.value = '';
            formCartinha.dispatchEvent(new Event('submit', { cancelable: true }));

            const erroNomeVisivel = !erroNome.classList.contains('d-none') && erroNome.textContent.trim().length > 0;
            const erroPedidosVisivel = !erroPedidos.classList.contains('d-none') && erroPedidos.textContent.trim().length > 0;
            const focoNoNome = (document.activeElement === inputNome);

            testResults.emptyValidationPassed = erroNomeVisivel && erroPedidosVisivel;
            testResults.firstErrorFocused = focoNoNome;

            // 4. Teste de Limpeza de Erro ao Digitar
            testResults.errorClearOnInputTested = true;
            inputNome.value = 'A';
            inputNome.dispatchEvent(new Event('input'));
            const erroNomeLimpo = erroNome.classList.contains('d-none') && !inputNome.classList.contains('is-invalid');

            inputPedidos.value = 'B';
            inputPedidos.dispatchEvent(new Event('input'));
            const erroPedidosLimpo = erroPedidos.classList.contains('d-none') && !inputPedidos.classList.contains('is-invalid');
            testResults.errorClearOnInputPassed = erroNomeLimpo && erroPedidosLimpo;

            // 5. Teste de Validação com Idade Inválida (negativa, decimal, > 120)
            testResults.invalidAgeTested = true;
            inputNome.value = 'Mariazinha';
            inputNome.dispatchEvent(new Event('input'));
            inputPedidos.value = 'Uma boneca mágica';
            inputPedidos.dispatchEvent(new Event('input'));

            // 5a. Idade negativa
            inputIdade.value = '-2';
            formCartinha.dispatchEvent(new Event('submit', { cancelable: true }));
            const erroIdadeNegativa = !erroIdade.classList.contains('d-none');

            // 5b. Idade decimal
            inputIdade.value = '7.5';
            formCartinha.dispatchEvent(new Event('submit', { cancelable: true }));
            const erroIdadeDecimal = !erroIdade.classList.contains('d-none');

            // 5c. Idade > 120
            inputIdade.value = '150';
            formCartinha.dispatchEvent(new Event('submit', { cancelable: true }));
            const erroIdadeMaior120 = !erroIdade.classList.contains('d-none');

            testResults.invalidAgePassed = erroIdadeNegativa && erroIdadeDecimal && erroIdadeMaior120;

            // 6. Teste de Concordância Gramatical da Idade (singular / plural / vazia)
            testResults.ageGrammarTested = true;
            // 6a. Idade 1 -> "1 ano"
            inputIdade.value = '1';
            inputIdade.dispatchEvent(new Event('input'));
            const textoIdade1 = paragrafoApresentacao.textContent;
            const gramaticaSingularOk = textoIdade1.includes('1 ano') && !textoIdade1.includes('1 anos');

            // 6b. Idade vazia -> omite "tenho ... anos"
            inputIdade.value = '';
            inputIdade.dispatchEvent(new Event('input'));
            const textoIdadeVazia = paragrafoApresentacao.textContent;
            const omissaoIdadeOk = !textoIdadeVazia.includes('tenho') && !textoIdadeVazia.includes('anos');

            testResults.ageGrammarPassed = gramaticaSingularOk && omissaoIdadeOk;

            // 7. Teste de Troca de Comportamento
            testResults.behaviorToggleTested = true;
            const radioTentei = document.getElementById('comportamento-tentei');
            const radioTravessura = document.getElementById('comportamento-travessura');
            const radioBonzinho = document.getElementById('comportamento-bonzinho');

            radioTentei.checked = true;
            radioTentei.dispatchEvent(new Event('change'));
            const textoTenteiOk = cartaComportamentoCont.textContent.includes('tentei bastante');

            radioTravessura.checked = true;
            radioTravessura.dispatchEvent(new Event('change'));
            const textoTravessuraOk = cartaComportamentoCont.textContent.includes('travessura');

            radioBonzinho.checked = true;
            radioBonzinho.dispatchEvent(new Event('change'));
            const textoBonzinhoOk = cartaComportamentoCont.textContent.includes('bonzinho');

            testResults.behaviorTogglePassed = textoTenteiOk && textoTravessuraOk && textoBonzinhoOk;

            // 8. Teste de Preenchimento Completo e Válido (e foco acessível no pergaminho)
            testResults.fullValidSubmissionTested = true;
            inputNome.value = 'João Gabriel';
            inputNome.dispatchEvent(new Event('input'));

            inputIdade.value = '8';
            inputIdade.dispatchEvent(new Event('input'));

            inputCidade.value = 'Florianópolis';
            inputCidade.dispatchEvent(new Event('input'));

            radioTentei.checked = true;
            radioTentei.dispatchEvent(new Event('change'));

            inputPedidos.value = 'Um trenzinho de madeira com trilhos e muita paz para minha família!';
            inputPedidos.dispatchEvent(new Event('input'));

            formCartinha.dispatchEvent(new Event('submit', { cancelable: true }));

            const sucessoVisivel = !document.getElementById('sucesso-validacao').classList.contains('d-none');
            const errosLimpos = erroNome.classList.contains('d-none') && erroIdade.classList.contains('d-none') && erroPedidos.classList.contains('d-none');

            const nomeRefletido = document.getElementById('carta-nome').textContent.includes('João Gabriel');
            const cartaIdadeEl = document.getElementById('carta-idade');
            const idadeRefletida = cartaIdadeEl ? cartaIdadeEl.textContent.includes('8') : false;
            const gramaticaPluralOk = paragrafoApresentacao.textContent.includes('8 anos');
            const cidadeRefletida = document.getElementById('carta-cidade').textContent.includes('Florianópolis');
            const pedidosRefletidos = cartaPedidos.textContent.includes('trenzinho de madeira');
            const comportamentoRefletido = cartaComportamentoCont.textContent.includes('tentei bastante');
            const assinaturaRefletida = cartaAssinatura.textContent.includes('João Gabriel') && cartaAssinatura.classList.contains('carta-assinatura-manuscrita');

            testResults.fullValidSubmissionPassed = sucessoVisivel && errosLimpos;
            testResults.letterReflectsAllData = nomeRefletido && idadeRefletida && gramaticaPluralOk && cidadeRefletida && pedidosRefletidos && comportamentoRefletido;
            testResults.handwrittenSignaturePassed = assinaturaRefletida;
            testResults.pergaminhoFocusedOnSuccess = (document.activeElement === pergaminhoCarta);

            // 9. Teste do Botão "Recomeçar" (#btn-limpar-cartinha)
            testResults.resetButtonTested = true;
            btnLimpar.click();

            const inputsLimpos = (inputNome.value === '') && (inputIdade.value === '') && (inputCidade.value === '') && (inputPedidos.value === '');
            const contadorResetado = (contadorCaracteres.textContent === '0/1000');
            const radioBonzinhoResetado = radioBonzinho.checked;
            const pergaminhoResetado = document.getElementById('carta-nome').textContent.includes('...') && cartaAssinatura.textContent.includes('...');
            const sucessoOcultoAposReset = document.getElementById('sucesso-validacao').classList.contains('d-none');
            const focoNoNomeAposReset = (document.activeElement === inputNome);

            testResults.resetButtonPassed = inputsLimpos && contadorResetado && radioBonzinhoResetado && pergaminhoResetado && sucessoOcultoAposReset && focoNoNomeAposReset;

        } catch (err) {
            testResults.errors.push(err.toString());
        }

        testResults.alertsUsed = window.__alertIntercepted || window.__confirmIntercepted;
        testResults.errors = testResults.errors.concat(window.__pageErrors);

        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;

        const payload = {
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight,
            scrollWidth: scrollWidth,
            clientWidth: clientWidth,
            hasOverflow: scrollWidth > clientWidth,
            testResults: testResults
        };

        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/report_s2?d=' + encodeURIComponent(JSON.stringify(payload)), false);
            xhr.send();
        } catch(e) {
            const img = new Image();
            img.src = '/api/report_s2?d=' + encodeURIComponent(JSON.stringify(payload));
        }
    });
    </script>
    """

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(html_code.replace("</body>", audit_s2_code + "\n</body>"))

    resolutions = [
        (360, 640, "Smartphone Pequeno (360px)"),
        (768, 1024, "Tablet / iPad (768px)"),
        (1920, 1080, "Desktop Full HD (1920px)")
    ]

    all_tests_passed = True
    print("\n[2/3] Executando interações dinâmicas e testes no Firefox Headless...")

    try:
        for width, height, device_name in resolutions:
            print(f"\n  -> Testando em {device_name} [{width}x{height}px]...")
            screenshot_dest = ARTIFACTS_DIR / f"screen_s2_{width}px.png"
            cmd = [
                "firefox",
                "--headless",
                f"--screenshot={screenshot_dest}",
                f"--window-size={width},{height}",
                f"http://127.0.0.1:{port}/test_runner_s2.html"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            time.sleep(1)

            matching = [r for r in received_reports if abs(r['viewportWidth'] - width) <= 25]
            if not matching:
                print(f"    ✗ FALHA: Nenhum relatório recebido do navegador para {width}px")
                all_tests_passed = False
                continue

            report = matching[-1]
            tr = report['testResults']

            # Verificação 1: Overflow
            if report['hasOverflow']:
                print(f"    ✗ ERRO: Rolagem horizontal detectada! scrollWidth={report['scrollWidth']} > clientWidth={report['clientWidth']}")
                all_tests_passed = False
            else:
                print(f"    ✓ Sem rolagem horizontal: scrollWidth ({report['scrollWidth']}px) <= clientWidth ({report['clientWidth']}px)")

            # Verificação 2: Dimensões dos cards de comportamento (>= 48px x 48px)
            if tr['cardDimensionsMeets48px']:
                print("    ✓ Todos os cards de comportamento atendem à área de toque mínima de 48px x 48px:")
                for c in tr['cardsAudited']:
                    print(f"      • Card '{c['text']}': {c['width']:.1f}px x {c['height']:.1f}px")
            else:
                print("    ✗ ERRO: Algum card de comportamento possui área menor que 48px x 48px!")
                all_tests_passed = False

            # Verificação 3: Sincronização em tempo real antes do submit
            if tr['realtimeSyncBeforeSubmitPassed']:
                print("    ✓ Sincronização em tempo real de digitação no pergaminho antes do submit confirmada.")
            else:
                print("    ✗ ERRO: Sincronização em tempo real antes do submit falhou!")
                all_tests_passed = False

            # Verificação 4: Contador de caracteres
            if tr['charCounterPassed']:
                print("    ✓ Contador dinâmico de caracteres atualizado com precisão.")
            else:
                print("    ✗ ERRO: Contador de caracteres falhou!")
                all_tests_passed = False

            # Verificação 5: Validação de campos vazios
            if tr['emptyValidationPassed']:
                print("    ✓ Validação gentil acionada em campos vazios com mensagens visuais acolhedoras.")
            else:
                print("    ✗ ERRO: Falha na validação de campos vazios!")
                all_tests_passed = False

            # Verificação 6: Foco suave no primeiro campo com erro
            if tr['firstErrorFocused']:
                print("    ✓ Foco colocado suavemente no primeiro campo com erro (#nome-crianca).")
            else:
                print("    ✗ AVISO/ERRO: Foco não estava no primeiro campo com pendência.")
                all_tests_passed = False

            # Verificação 7: Limpeza de erro ao digitar
            if tr['errorClearOnInputPassed']:
                print("    ✓ Erros visuais e classes is-invalid limpos imediatamente ao digitar valor válido.")
            else:
                print("    ✗ ERRO: Limpeza de erro ao digitar falhou!")
                all_tests_passed = False

            # Verificação 8: Validação de idade abrangente (negativa, decimal, > 120)
            if tr['invalidAgePassed']:
                print("    ✓ Validação estrita de idade (rejeita negativa, decimal e > 120) funcionando.")
            else:
                print("    ✗ ERRO: Validação de idade inválida falhou!")
                all_tests_passed = False

            # Verificação 9: Concordância gramatical da idade (singular/plural/omissão)
            if tr['ageGrammarPassed']:
                print("    ✓ Concordância gramatical da idade impecável ('1 ano', '8 anos', e omissão limpa se vazia).")
            else:
                print("    ✗ ERRO: Concordância gramatical da idade no pergaminho falhou!")
                all_tests_passed = False

            # Verificação 10: Troca dinâmica de comportamento
            if tr['behaviorTogglePassed']:
                print("    ✓ Troca dinâmica de comportamento atualiza imediatamente a cartinha com textos e ícones correspondentes.")
            else:
                print("    ✗ ERRO: Sincronização do seletor de comportamento com a cartinha falhou!")
                all_tests_passed = False

            # Verificação 11: Preenchimento completo e montagem da carta
            if tr['fullValidSubmissionPassed'] and tr['letterReflectsAllData']:
                print("    ✓ Submissão válida: pergaminho reflete nome, idade, cidade, comportamento e pedidos sem recarregar.")
            else:
                print(f"    ✗ ERRO: Montagem da cartinha com dados completos falhou! (passed={tr['fullValidSubmissionPassed']}, reflects={tr['letterReflectsAllData']})")
                all_tests_passed = False

            # Verificação 12: Assinatura manuscrita temática
            if tr['handwrittenSignaturePassed']:
                print("    ✓ Assinatura manuscrita temática (#carta-assinatura) renderizada com elegância.")
            else:
                print("    ✗ ERRO: Assinatura manuscrita falhou!")
                all_tests_passed = False

            # Verificação 13: Foco acessível no pergaminho após sucesso
            if tr['pergaminhoFocusedOnSuccess']:
                print("    ✓ Foco acessível transferido para o pergaminho (#pergaminho-carta) após submissão válida.")
            else:
                print("    ✗ ERRO: Foco não foi transferido para o pergaminho após sucesso!")
                all_tests_passed = False

            # Verificação 14: Botão "Recomeçar" (#btn-limpar-cartinha)
            if tr['resetButtonPassed']:
                print("    ✓ Botão 'Recomeçar' limpa formulário, reseta comportamento, restaura pergaminho e devolve o foco ao nome.")
            else:
                print("    ✗ ERRO: Teste do botão 'Recomeçar' falhou!")
                all_tests_passed = False

            # Verificação 15: Sem alerts nativos
            if not tr['alertsUsed']:
                print("    ✓ Nenhum alert() ou confirm() nativo intrusivo acionado.")
            else:
                print("    ✗ ERRO: alert() ou confirm() nativo foi utilizado!")
                all_tests_passed = False

            # Verificação 16: Erros de console / página
            if not tr['errors']:
                print("    ✓ Zero erros ou exceções no console.")
            else:
                print(f"    ✗ ERRO: Erros de console: {tr['errors']}")
                all_tests_passed = False

    finally:
        if test_file_path.exists():
            test_file_path.unlink()
        server.shutdown()
        server.server_close()

    print("\n=================================================================")
    if all_tests_passed:
        print(" RESULTADO HISTÓRIA 2: TODOS OS TESTES PASSARAM COM SUCESSO! 🎉")
        print("=================================================================")
        sys.exit(0)
    else:
        print(" RESULTADO HISTÓRIA 2: ALGUNS TESTES FALHARAM ❌")
        print("=================================================================")
        sys.exit(1)

if __name__ == '__main__':
    main()
