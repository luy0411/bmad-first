#!/usr/bin/env python3
"""
Testes automatizados dos critérios de aceitação da História 4:
- Impressão estilizada da cartinha como lembrança física (CAP-5)
- Presença do botão temático "Imprimir / Guardar Lembrança" (#btn-imprimir-cartinha) nas ações do formulário
- Presença do botão complementar de impressão no modal do Papai Noel (#btn-imprimir-modal)
- Área de toque mínima de 48px x 48px nos botões de impressão em todas as resoluções
- Acionamento nativo de window.print() sem recarregamento de página
- Regras @media print no CSS que ocultam controles funcionais web (.festive-header, #form-carta, .modal, .btn, #snow-container, .festive-footer)
- Formatação estilizada do pergaminho (#pergaminho-carta) para impressão limpa, legível e econômica
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
        if self.path.startswith('/api/report_s4'):
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
    print(" INICIANDO VERIFICAÇÃO AUTOMATIZADA - HISTÓRIA 4 (IMPRESSÃO FÍSICA)")
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

    network_forbidden = ["fetch(", "XMLHttpRequest", "axios", "$.ajax", "navigator.sendBeacon"]
    for net in network_forbidden:
        if net in js_code:
            print(f"  ✗ ERRO: Chamada de rede ({net}) detectada no js/app.js! Arquitetura deve ser 100% client-side.")
            sys.exit(1)
    print("  ✓ Arquitetura 100% client-side sem chamadas a servidores externos.")

    # Verificar chamada window.print() no js/app.js
    if "window.print()" not in js_code and "print()" not in js_code:
        print("  ✗ ERRO: Invocação de window.print() ausente no js/app.js!")
        sys.exit(1)
    print("  ✓ Invocação nativa de window.print() configurada no js/app.js.")

    # Verificar elementos HTML obrigatórios
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html_code = f.read()

    required_html_elements = [
        ('id="btn-imprimir-cartinha"', 'Botão de impressão principal #btn-imprimir-cartinha'),
        ('id="btn-imprimir-modal"', 'Botão de impressão no modal #btn-imprimir-modal'),
        ('btn-imprimir-natal', 'Classe estética .btn-imprimir-natal nos botões de impressão'),
        ('id="pergaminho-carta"', 'Pergaminho da cartinha #pergaminho-carta')
    ]
    for pattern, desc in required_html_elements:
        if pattern in html_code:
            print(f"  ✓ {desc} presente no index.html.")
        else:
            print(f"  ✗ ERRO: {desc} ({pattern}) ausente no index.html!")
            sys.exit(1)

    # Verificar regras CSS obrigatórias (@media print)
    with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
        css_code = f.read()

    if "@media print" not in css_code:
        print("  ✗ ERRO: Bloco @media print ausente no style.css!")
        sys.exit(1)
    print("  ✓ Bloco @media print configurado no style.css.")

    required_print_tokens = [
        ("display: none", "Ocultação de elementos na folha física"),
        (".btn-imprimir-natal", "Estilização do botão temático de impressão"),
        ("page-break-inside", "Controle de quebra de página (page-break-inside)"),
        ("#pergaminho-carta", "Escopamento da cartinha para impressão")
    ]
    for token, desc in required_print_tokens:
        if token in css_code:
            print(f"  ✓ Regra CSS para {desc} ('{token}') presente no style.css.")
        else:
            print(f"  ✗ ERRO: Regra CSS para {desc} ('{token}') ausente no style.css!")
            sys.exit(1)

    # -------------------------------------------------------------
    # 2. Inicialização do Servidor HTTP Local para Teste no Browser
    # -------------------------------------------------------------
    port = get_free_port()
    server = start_server(port)
    time.sleep(0.4)

    test_file_path = BASE_DIR / "test_runner_s4.html"

    audit_s4_code = """
    <script>
    window.__pageErrors = [];
    window.__printCount = 0;
    window.__mockPrint = function() {
        window.__printCount++;
    };

    window.addEventListener('error', (e) => {
        window.__pageErrors.push(e.message);
    });

    try {
        window.print = function() {
            window.__printCount++;
        };
        Object.defineProperty(window, 'print', {
            value: function() { window.__printCount++; },
            writable: true,
            configurable: true
        });
    } catch(e) {}

    document.addEventListener('DOMContentLoaded', () => {
        const testResults = {
            touchTargetsMeets48px: true,
            targetsAudited: [],
            printBtnMainExists: false,
            printBtnModalExists: false,
            printMainTriggered: false,
            printModalTriggered: false,
            printRulesChecked: false,
            errors: []
        };

        try {
            const btnPrintMain = document.getElementById('btn-imprimir-cartinha');
            const btnPrintModal = document.getElementById('btn-imprimir-modal');
            const modalEl = document.getElementById('modal-papai-noel');

            if (btnPrintMain) testResults.printBtnMainExists = true;
            if (btnPrintModal) testResults.printBtnModalExists = true;

            // 1. Auditoria de ergonomia no botão principal
            if (btnPrintMain) {
                const rect = btnPrintMain.getBoundingClientRect();
                const meets = rect.width >= 47.5 && rect.height >= 47.5;
                if (!meets) testResults.touchTargetsMeets48px = false;
                testResults.targetsAudited.push({
                    name: 'Botão Imprimir Cartinha (Principal)',
                    width: rect.width,
                    height: rect.height,
                    meets48px: meets
                });
            }

            // Testar clique no botão principal
            if (btnPrintMain) {
                const initialCount = window.__printCount;
                btnPrintMain.click();
                if (window.__printCount > initialCount) {
                    testResults.printMainTriggered = true;
                }
            }

            // 2. Abertura do modal para auditoria e teste do botão de impressão do modal
            if (modalEl) {
                modalEl.classList.remove('fade');
                modalEl.classList.add('show');
                modalEl.style.display = 'block';
            }

            if (btnPrintModal) {
                const rectModalBtn = btnPrintModal.getBoundingClientRect();
                const meetsModal = rectModalBtn.width >= 47.5 && rectModalBtn.height >= 47.5;
                if (!meetsModal) testResults.touchTargetsMeets48px = false;
                testResults.targetsAudited.push({
                    name: 'Botão Imprimir Modal (Rodapé)',
                    width: rectModalBtn.width,
                    height: rectModalBtn.height,
                    meets48px: meetsModal
                });

                const initialModalCount = window.__printCount;
                btnPrintModal.click();
                if (window.__printCount > initialModalCount) {
                    testResults.printModalTriggered = true;
                }
            }

            if (modalEl) {
                modalEl.classList.remove('show');
                modalEl.style.display = 'none';
            }

            // Verificar se as regras CSS para print existem no document.styleSheets
            let foundPrintMedia = false;
            for (let i = 0; i < document.styleSheets.length; i++) {
                try {
                    const sheet = document.styleSheets[i];
                    const rules = sheet.cssRules || sheet.rules;
                    if (!rules) continue;
                    for (let j = 0; j < rules.length; j++) {
                        const rule = rules[j];
                        if (rule.media && rule.media.mediaText.includes('print')) {
                            foundPrintMedia = true;
                            break;
                        }
                    }
                } catch(e) {}
            }
            testResults.printRulesChecked = foundPrintMedia;

        } catch (err) {
            testResults.errors.push(err.toString());
        }

        const clientWidth = document.documentElement.clientWidth;
        const scrollWidth = document.documentElement.scrollWidth;
        const payload = {
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight,
            scrollWidth: scrollWidth,
            clientWidth: clientWidth,
            hasOverflow: scrollWidth > clientWidth,
            pageErrors: window.__pageErrors,
            testResults: testResults
        };

        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/report_s4?d=' + encodeURIComponent(JSON.stringify(payload)), false);
            xhr.send();
        } catch(e) {
            const img = new Image();
            img.src = '/api/report_s4?d=' + encodeURIComponent(JSON.stringify(payload));
        }
    });
    </script>
    """

    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        original_html = f.read()

    injected_html = original_html.replace("</body>", f"{audit_s4_code}\n</body>")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(injected_html)

    # -------------------------------------------------------------
    # 3. Execução no Firefox Headless para múltiplos viewports
    # -------------------------------------------------------------
    print("\n[2/3] Executando interações dinâmicas e testes no Firefox Headless...")

    viewports = [
        {"name": "Smartphone Pequeno (360px)", "w": 360, "h": 640},
        {"name": "Tablet / iPad (768px)", "w": 768, "h": 1024},
        {"name": "Desktop Full HD (1920px)", "w": 1920, "h": 1080}
    ]

    all_tests_passed = True

    # Garantir perfil temporário isolado para execuções sequenciais do Firefox sem lock
    subprocess.run(["firefox", "-CreateProfile", "bmad_test_profile /tmp/bmad_ff_prof"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        for vp in viewports:
            print(f"\n  -> Testando em {vp['name']} [{vp['w']}x{vp['h']}px]...")
            screenshot_dest = ARTIFACTS_DIR / f"screen_s4_{vp['w']}px.png"
            cmd = [
                "firefox",
                "--headless",
                "-no-remote",
                "-P", "bmad_test_profile",
                f"--screenshot={screenshot_dest}",
                f"--window-size={vp['w']},{vp['h']}",
                f"http://127.0.0.1:{port}/test_runner_s4.html"
            ]

            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            time.sleep(0.8)

            if len(received_reports) == 0:
                print(f"  ✗ ERRO: Não recebemos relatório do navegador em {vp['name']} dentro do tempo limite!")
                all_tests_passed = False
                continue

            report = received_reports.pop()
            res = report["testResults"]

            if report["hasOverflow"]:
                print(f"  ✗ ERRO: Rolagem horizontal detectada! scrollWidth ({report['scrollWidth']}px) > clientWidth ({report['clientWidth']}px)")
                all_tests_passed = False
            else:
                print(f"  ✓ Sem rolagem horizontal: scrollWidth ({report['scrollWidth']}px) <= clientWidth ({report['clientWidth']}px)")

            if not res["touchTargetsMeets48px"]:
                print("  ✗ ERRO: Botões de impressão violam área mínima de 48px x 48px:")
                for target in res["targetsAudited"]:
                    status = "✓" if target["meets48px"] else "✗"
                    print(f"    {status} {target['name']}: {target['width']:.1f}px x {target['height']:.1f}px")
                all_tests_passed = False
            else:
                print("  ✓ Botões de impressão atendem à área mínima de 48px x 48px:")
                for target in res["targetsAudited"]:
                    print(f"    • {target['name']}: {target['width']:.1f}px x {target['height']:.1f}px")

            if not res["printMainTriggered"]:
                print("  ✗ ERRO: Clique em #btn-imprimir-cartinha não disparou window.print()!")
                all_tests_passed = False
            else:
                print("  ✓ Clique no botão principal disparou window.print() com sucesso.")

            if not res["printModalTriggered"]:
                print("  ✗ ERRO: Clique em #btn-imprimir-modal não disparou window.print()!")
                all_tests_passed = False
            else:
                print("  ✓ Clique no botão do modal disparou window.print() com sucesso.")

            if not res["printRulesChecked"]:
                print("  ✗ ERRO: Regras @media print não encontradas no document.styleSheets!")
                all_tests_passed = False
            else:
                print("  ✓ Regras @media print ativas e verificadas nas folhas de estilo.")

            if len(report["pageErrors"]) > 0:
                print(f"  ✗ ERRO: Erros de console detectados: {report['pageErrors']}")
                all_tests_passed = False
            else:
                print("  ✓ Zero erros ou exceções no console JavaScript.")

    finally:
        if test_file_path.exists():
            test_file_path.unlink()
        server.shutdown()
        server.server_close()

    print("\n[3/3] Avaliação final dos critérios de aceitação...")
    if all_tests_passed:
        print("\n=================================================================")
        print(" RESULTADO HISTÓRIA 4: TODOS OS TESTES PASSARAM COM SUCESSO! 🎉")
        print("=================================================================\n")
        sys.exit(0)
    else:
        print("\n=================================================================")
        print(" RESULTADO HISTÓRIA 4: FALHA EM CRITÉRIOS DE ACEITAÇÃO! ❌")
        print("=================================================================\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
