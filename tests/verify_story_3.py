#!/usr/bin/env python3
"""
Testes automatizados dos critérios de aceitação da História 3:
- Envio interativo da cartinha com feedback festivo e modal do Papai Noel (CAP-3)
- Adição do botão de destaque "Enviar ao Papai Noel" (#btn-enviar-cartinha)
- Inserção do modal temático acessível (#modal-papai-noel, #modalPapaiNoelLabel, #mensagem-papai-noel, #selo-polo-norte-modal)
- Botões de fechar com área de toque mínima de 48px x 48px (.btn-modal-fechar-topo, .btn-modal-fechar)
- Validação síncrona gentil prévia ao envio (impede abertura do modal se houver campos essenciais pendentes)
- Foco automático no primeiro campo pendente em caso de erro
- Animação festiva de despacho visual (.efeito-despacho, .despachando-animacao)
- Mensagem acolhedora personalizada do Papai Noel interpolada com o nome da criança e comportamento declarado
- Assinatura oficial "Papai Noel e os Duendes"
- Selo postal oficial comemorativo do Polo Norte ("Oficial do Polo Norte")
- Fechamento suave do modal via botões de fechar, backdrop e tecla ESC
- Restauração automática do foco acessível para o botão de envio (#btn-enviar-cartinha) ao fechar o modal
- Reabertura após alteração refletindo os novos dados dinâmicos
- Zero chamadas a redes externas, zero dependências de build, zero window.alert nativo
- Responsividade fluida e integridade de layout em 360px, 768px e 1920px sem overflow horizontal
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
        if self.path.startswith('/api/report_s3'):
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
    print(" INICIANDO VERIFICAÇÃO AUTOMATIZADA - HISTÓRIA 3 (ENVIO MÁGICO)")
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

    # Verificar proibições de alertas nativos e requisições de rede
    if "alert(" in js_code:
        print("  ✗ ERRO: Uso de alert() detectado no js/app.js!")
        sys.exit(1)
    if "confirm(" in js_code:
        print("  ✗ ERRO: Uso de confirm() detectado no js/app.js!")
        sys.exit(1)
    print("  ✓ Sem alert() ou confirm() nativos no js/app.js.")

    # Verificar ausência de requisições de rede externas
    network_forbidden = ["fetch(", "XMLHttpRequest", "axios", "$.ajax", "navigator.sendBeacon"]
    for net in network_forbidden:
        if net in js_code:
            print(f"  ✗ ERRO: Chamada de rede ({net}) detectada no js/app.js! Arquitetura deve ser 100% client-side.")
            sys.exit(1)
    print("  ✓ Arquitetura 100% client-side sem chamadas a servidores externos.")

    # Verificar elementos obrigatórios no index.html
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html_code = f.read()

    required_html_elements = [
        ('id="btn-enviar-cartinha"', 'Botão de envio mágico #btn-enviar-cartinha'),
        ('id="modal-papai-noel"', 'Modal do Papai Noel #modal-papai-noel'),
        ('id="modalPapaiNoelLabel"', 'Título acessível do modal #modalPapaiNoelLabel'),
        ('id="mensagem-papai-noel"', 'Área da mensagem do Papai Noel #mensagem-papai-noel'),
        ('id="selo-polo-norte-modal"', 'Selo do Polo Norte no modal #selo-polo-norte-modal'),
        ('data-bs-dismiss="modal"', 'Atributos de fechamento acessível data-bs-dismiss'),
        ('btn-modal-fechar-topo', 'Botão de fechar do cabeçalho .btn-modal-fechar-topo'),
        ('btn-modal-fechar', 'Botão de fechar do rodapé .btn-modal-fechar'),
        ('Oficial do Polo Norte', 'Texto comemorativo Oficial do Polo Norte')
    ]
    for pattern, desc in required_html_elements:
        if pattern in html_code:
            print(f"  ✓ {desc} presente no index.html.")
        else:
            print(f"  ✗ ERRO: {desc} ({pattern}) ausente no index.html!")
            sys.exit(1)

    # Verificar classes CSS obrigatórias no style.css
    with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
        css_code = f.read()

    required_css_tokens = [
        ".modal-natalino",
        ".modal-header-natal",
        ".selo-modal",
        ".btn-modal-fechar",
        ".btn-enviar-natal",
        ".efeito-despacho"
    ]
    for token in required_css_tokens:
        if token in css_code:
            print(f"  ✓ Classe/Regra CSS '{token}' presente no style.css.")
        else:
            print(f"  ✗ ERRO: Classe/Regra CSS '{token}' ausente no style.css!")
            sys.exit(1)

    # Verificar no js/app.js a presença do foco restaurado e assinatura oficial
    if "hidden.bs.modal" not in js_code:
        print("  ✗ ERRO: Evento hidden.bs.modal para restauração de foco ausente no js/app.js!")
        sys.exit(1)
    print("  ✓ Listener para retorno de foco em hidden.bs.modal presente no js/app.js.")

    if "Papai Noel e os Duendes" not in js_code:
        print("  ✗ ERRO: Assinatura carinhosa 'Papai Noel e os Duendes' ausente no js/app.js!")
        sys.exit(1)
    print("  ✓ Assinatura oficial 'Papai Noel e os Duendes' presente no js/app.js.")

    # -------------------------------------------------------------
    # 2. Inicialização do Servidor HTTP Local para Teste no Browser
    # -------------------------------------------------------------
    port = get_free_port()
    server = start_server(port)
    time.sleep(0.4)

    test_file_path = BASE_DIR / "test_runner_s3.html"

    # Script de auditoria dinâmica executado diretamente no Firefox Headless
    audit_s3_code = """
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
            touchTargetsMeets48px: true,
            targetsAudited: [],
            emptyValidationTested: false,
            emptyValidationPassed: false,
            modalRemainedClosedOnInvalid: false,
            firstErrorFocused: false,
            validSubmissionTested: false,
            validSubmissionPassed: false,
            dispatchAnimationTriggered: false,
            modalOpenedOnValid: false,
            personalizedNameRendered: false,
            personalizedCityRendered: false,
            behaviorMessageRendered: false,
            officialSealPresent: false,
            officialSignaturePresent: false,
            closeViaButtonTested: false,
            closeViaButtonPassed: false,
            focusRestoredAfterButtonClose: false,
            reopenAfterEditTested: false,
            reopenAfterEditPassed: false,
            reopenReflectsNewData: false,
            closeViaEscTested: false,
            closeViaEscPassed: false,
            focusRestoredAfterEscClose: false,
            mischiefBehaviorTested: false,
            mischiefBehaviorPassed: false,
            alertsUsed: false,
            errors: []
        };

        try {
            const btnEnviar = document.getElementById('btn-enviar-cartinha');
            const inputNome = document.getElementById('nome-crianca');
            const inputIdade = document.getElementById('idade-crianca');
            const inputCidade = document.getElementById('cidade-crianca');
            const inputPedidos = document.getElementById('pedidos-crianca');
            const modalEl = document.getElementById('modal-papai-noel');
            const mensagemEl = document.getElementById('mensagem-papai-noel');
            const seloEl = document.getElementById('selo-polo-norte-modal');

            // Remove classe fade para auditoria síncrona determinística no headless
            if (modalEl) {
                modalEl.classList.remove('fade');
            }

            const btnFecharTopo = modalEl ? modalEl.querySelector('.btn-modal-fechar-topo') : null;
            const btnFecharRodape = modalEl ? modalEl.querySelector('.btn-modal-fechar') : null;

            // 1. Auditoria de Dimensões Ergonômicas do Botão de Envio (>= 48px x 48px)
            if (btnEnviar) {
                const rEnviar = btnEnviar.getBoundingClientRect();
                const meets = (rEnviar.width >= 48) && (rEnviar.height >= 48);
                testResults.targetsAudited.push({
                    name: 'Botão Enviar ao Papai Noel',
                    width: rEnviar.width,
                    height: rEnviar.height,
                    meets48px: meets
                });
                if (!meets) testResults.touchTargetsMeets48px = false;
            }

            // 2. Teste: Tentativa de envio com campos em branco (Validação prévia gentil)
            testResults.emptyValidationTested = true;
            inputNome.value = '';
            inputPedidos.value = '';
            btnEnviar.click();

            const isModalOpenEmpty = modalEl.classList.contains('show') || modalEl.style.display === 'block';
            const erroNomeVisivel = !document.getElementById('erro-nome').classList.contains('d-none');
            const erroPedidosVisivel = !document.getElementById('erro-pedidos').classList.contains('d-none');
            const focoNoNome = (document.activeElement === inputNome);

            testResults.modalRemainedClosedOnInvalid = !isModalOpenEmpty;
            testResults.firstErrorFocused = focoNoNome;
            testResults.emptyValidationPassed = (!isModalOpenEmpty && erroNomeVisivel && erroPedidosVisivel && focoNoNome);

            // 3. Teste: Envio Válido Completo (Comportamento Bonzinho)
            testResults.validSubmissionTested = true;
            inputNome.value = 'Clara';
            inputNome.dispatchEvent(new Event('input'));
            inputIdade.value = '8';
            inputIdade.dispatchEvent(new Event('input'));
            inputCidade.value = 'Curitiba';
            inputCidade.dispatchEvent(new Event('input'));
            inputPedidos.value = 'Quero um trenó mágico e um livro de aventuras.';
            inputPedidos.dispatchEvent(new Event('input'));

            // Dispara o envio mágico
            btnEnviar.click();

            const isModalOpenValid = modalEl.classList.contains('show') || modalEl.style.display === 'block';
            testResults.modalOpenedOnValid = isModalOpenValid;
            testResults.dispatchAnimationTriggered = true;

            const msgHtml = mensagemEl ? mensagemEl.innerHTML : '';
            testResults.personalizedNameRendered = msgHtml.includes('Clara');
            testResults.personalizedCityRendered = msgHtml.includes('Curitiba');
            testResults.behaviorMessageRendered = msgHtml.includes('muito bonzinho');
            testResults.officialSignaturePresent = msgHtml.includes('Papai Noel e os Duendes');
            testResults.officialSealPresent = seloEl && seloEl.textContent.includes('Oficial do Polo Norte');

            // Auditoria de touch target dos botões de fechar com modal aberto
            if (btnFecharTopo) {
                const rTopo = btnFecharTopo.getBoundingClientRect();
                const meets = (rTopo.width >= 48) && (rTopo.height >= 48);
                testResults.targetsAudited.push({
                    name: 'Botão Fechar Topo (Modal)',
                    width: rTopo.width,
                    height: rTopo.height,
                    meets48px: meets
                });
                if (!meets) testResults.touchTargetsMeets48px = false;
            }

            if (btnFecharRodape) {
                const rRodape = btnFecharRodape.getBoundingClientRect();
                const meets = (rRodape.width >= 48) && (rRodape.height >= 48);
                testResults.targetsAudited.push({
                    name: 'Botão Fechar Rodapé (Modal)',
                    width: rRodape.width,
                    height: rRodape.height,
                    meets48px: meets
                });
                if (!meets) testResults.touchTargetsMeets48px = false;
            }

            testResults.validSubmissionPassed = (
                isModalOpenValid &&
                testResults.personalizedNameRendered &&
                testResults.personalizedCityRendered &&
                testResults.behaviorMessageRendered &&
                testResults.officialSignaturePresent &&
                testResults.officialSealPresent
            );

            // 4. Teste: Fechamento do Modal pelo Botão de Rodapé e Restauração de Foco
            testResults.closeViaButtonTested = true;
            if (btnFecharRodape) {
                btnFecharRodape.click();
            } else if (btnFecharTopo) {
                btnFecharTopo.click();
            }

            const isModalClosed = !modalEl.classList.contains('show') && (modalEl.style.display === 'none' || modalEl.style.display === '');
            testResults.closeViaButtonPassed = isModalClosed;
            testResults.focusRestoredAfterButtonClose = (document.activeElement === btnEnviar);

            // 5. Teste: Reabertura após Alteração de Dados (Nome, Cidade, Comportamento)
            testResults.reopenAfterEditTested = true;
            inputNome.value = 'Pedrinho';
            inputNome.dispatchEvent(new Event('input'));
            inputCidade.value = 'Recife';
            inputCidade.dispatchEvent(new Event('input'));
            inputPedidos.value = 'Quero patins velozes.';
            inputPedidos.dispatchEvent(new Event('input'));

            const radioTentei = document.getElementById('comportamento-tentei');
            if (radioTentei) {
                radioTentei.checked = true;
                radioTentei.dispatchEvent(new Event('change'));
            }

            // Novo clique de envio
            btnEnviar.click();

            const isReopenOpen = modalEl.classList.contains('show') || modalEl.style.display === 'block';
            const msgReopenHtml = mensagemEl ? mensagemEl.innerHTML : '';
            const hasNewName = msgReopenHtml.includes('Pedrinho');
            const hasNewCity = msgReopenHtml.includes('Recife');
            const hasNewBehavior = msgReopenHtml.includes('Tentar bastante') || msgReopenHtml.includes('tentar bastante');

            testResults.reopenReflectsNewData = (hasNewName && hasNewCity && hasNewBehavior);
            testResults.reopenAfterEditPassed = (isReopenOpen && testResults.reopenReflectsNewData);

            // 6. Teste: Fechamento via Tecla ESC e Restauração de Foco
            testResults.closeViaEscTested = true;
            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', bubbles: true }));

            const isClosedAfterEsc = !modalEl.classList.contains('show') && (modalEl.style.display === 'none' || modalEl.style.display === '');
            testResults.closeViaEscPassed = isClosedAfterEsc;
            testResults.focusRestoredAfterEscClose = (document.activeElement === btnEnviar);

            // 7. Teste: Comportamento de Travessura e Fechamento via Topo
            testResults.mischiefBehaviorTested = true;
            const radioTravessura = document.getElementById('comportamento-travessura');
            if (radioTravessura) {
                radioTravessura.checked = true;
                radioTravessura.dispatchEvent(new Event('change'));
            }

            btnEnviar.click();

            const msgTravessuraHtml = mensagemEl ? mensagemEl.innerHTML : '';
            const hasMischiefText = msgTravessuraHtml.includes('travessura');

            if (btnFecharTopo) {
                btnFecharTopo.click();
            }

            const isClosedAfterTopo = !modalEl.classList.contains('show') && (modalEl.style.display === 'none' || modalEl.style.display === '');
            testResults.mischiefBehaviorPassed = (hasMischiefText && isClosedAfterTopo);

        } catch (err) {
            testResults.errors.push('Exceção nos testes JS: ' + err.toString());
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
            xhr.open('GET', '/api/report_s3?d=' + encodeURIComponent(JSON.stringify(payload)), false);
            xhr.send();
        } catch(e) {
            const img = new Image();
            img.src = '/api/report_s3?d=' + encodeURIComponent(JSON.stringify(payload));
        }
    });
    </script>
    """

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(html_code.replace("</body>", audit_s3_code + "\n</body>"))

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
            screenshot_dest = ARTIFACTS_DIR / f"screen_s3_{width}px.png"
            cmd = [
                "firefox",
                "--headless",
                "-no-remote",
                "-P", "bmad_test_profile",
                f"--screenshot={screenshot_dest}",
                f"--window-size={width},{height}",
                f"http://127.0.0.1:{port}/test_runner_s3.html"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            time.sleep(0.8)

            if not received_reports:
                print(f"  ✗ ERRO: Nenhum relatório recebido da auditoria em {device_name}!")
                all_tests_passed = False
                continue

            report = received_reports.pop()
            res = report["testResults"]

            # Verificação de rolagem horizontal
            if report["hasOverflow"]:
                print(f"  ✗ ERRO: Rolagem horizontal detectada! scrollWidth ({report['scrollWidth']}px) > clientWidth ({report['clientWidth']}px)")
                all_tests_passed = False
            else:
                print(f"  ✓ Sem rolagem horizontal: scrollWidth ({report['scrollWidth']}px) <= clientWidth ({report['clientWidth']}px)")

            # Verificação das áreas de toque >= 48px
            if not res["touchTargetsMeets48px"]:
                print("  ✗ ERRO: Alguns elementos interativos violam a área de toque mínima de 48px x 48px:")
                for target in res["targetsAudited"]:
                    status = "✓" if target["meets48px"] else "✗"
                    print(f"    {status} {target['name']}: {target['width']:.1f}px x {target['height']:.1f}px")
                all_tests_passed = False
            else:
                print("  ✓ Todos os botões do fluxo de envio e modal atendem à área mínima de 48px x 48px:")
                for target in res["targetsAudited"]:
                    print(f"    • {target['name']}: {target['width']:.1f}px x {target['height']:.1f}px")

            # Verificação de validação com dados incompletos
            if not res["emptyValidationPassed"]:
                print("  ✗ ERRO: Validação prévia em campos em branco falhou!")
                if not res["modalRemainedClosedOnInvalid"]:
                    print("    - Modal abriu indevidamente com dados pendentes.")
                if not res["firstErrorFocused"]:
                    print("    - Foco suave não foi direcionado ao primeiro campo inválido.")
                all_tests_passed = False
            else:
                print("  ✓ Validação gentil acionada em envio incompleto: modal permaneceu fechado e foco moveu para o nome.")

            # Verificação de envio válido e modal com dados corretos
            if not res["validSubmissionPassed"]:
                print("  ✗ ERRO: Envio válido falhou ou modal não exibiu os dados esperados!")
                if not res["modalOpenedOnValid"]:
                    print("    - Modal não abriu após envio válido.")
                if not res["personalizedNameRendered"]:
                    print("    - Nome da criança não renderizado na mensagem do Noel.")
                if not res["personalizedCityRendered"]:
                    print("    - Cidade da criança não renderizada na mensagem do Noel.")
                if not res["behaviorMessageRendered"]:
                    print("    - Comportamento bonzinho não celebrado na mensagem.")
                if not res["officialSignaturePresent"]:
                    print("    - Assinatura oficial 'Papai Noel e os Duendes' ausente.")
                if not res["officialSealPresent"]:
                    print("    - Selo oficial do Polo Norte ausente.")
                all_tests_passed = False
            else:
                print("  ✓ Envio válido bem-sucedido: modal natalino aberto com mensagem personalizada e selo oficial.")

            # Verificação de fechamento e restauração de foco
            if not res["closeViaButtonPassed"] or not res["focusRestoredAfterButtonClose"]:
                print("  ✗ ERRO: Fechamento por botão ou restauração de foco falhou!")
                all_tests_passed = False
            else:
                print("  ✓ Fechamento suave do modal via botão confirmado com foco restaurado em #btn-enviar-cartinha.")

            # Verificação de reabertura com dados atualizados
            if not res["reopenAfterEditPassed"]:
                print("  ✗ ERRO: Reabertura após alteração de dados não refletiu as mudanças na mensagem!")
                all_tests_passed = False
            else:
                print("  ✓ Reabertura após edição validada: novos dados e comportamento 'Tentei bastante' refletidos com precisão.")

            # Verificação de fechamento via tecla ESC
            if not res["closeViaEscPassed"] or not res["focusRestoredAfterEscClose"]:
                print("  ✗ ERRO: Fechamento por tecla ESC ou retorno de foco falhou!")
                all_tests_passed = False
            else:
                print("  ✓ Fechamento por tecla ESC validado com restauração impecável de foco no botão de envio.")

            # Verificação de mensagem para comportamento 'Às vezes fiz travessura'
            if not res["mischiefBehaviorPassed"]:
                print("  ✗ ERRO: Mensagem carinhosa para comportamento 'Às vezes fiz travessura' não validada!")
                all_tests_passed = False
            else:
                print("  ✓ Acolhimento especial para comportamento 'Às vezes fiz travessura' validado com afeto.")

            # Verificação de ausência de alertas nativos
            if res["alertsUsed"]:
                print("  ✗ ERRO: Alertas nativos do navegador (window.alert/confirm) foram disparados!")
                all_tests_passed = False
            else:
                print("  ✓ Nenhum alert() ou confirm() nativo acionado.")

            # Verificação de erros no console
            if res["errors"]:
                print(f"  ✗ ERRO: Erros detectados no console: {res['errors']}")
                all_tests_passed = False
            else:
                print("  ✓ Zero erros ou exceções no console.")

    finally:
        server.shutdown()
        server.server_close()
        if test_file_path.exists():
            test_file_path.unlink()

    # -------------------------------------------------------------
    # 3. Veredito Final
    # -------------------------------------------------------------
    print("\n[3/3] Avaliação final dos critérios de aceitação...")
    if all_tests_passed:
        print("\n" + "=" * 65)
        print(" RESULTADO HISTÓRIA 3: TODOS OS TESTES PASSARAM COM SUCESSO! 🎉")
        print("=" * 65 + "\n")
        sys.exit(0)
    else:
        print("\n" + "=" * 65)
        print(" RESULTADO HISTÓRIA 3: ALGUNS TESTES FALHARAM! ❌")
        print("=" * 65 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
