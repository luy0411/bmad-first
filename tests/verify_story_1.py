#!/usr/bin/env python3
"""
Testes automatizados dos critérios de aceitação da História 1:
- Tema natalino e variáveis CSS (:root)
- Animação de neve em CSS puro com pointer-events: none e will-change
- Presença e propriedades dos elementos .snowflake no DOM
- Validação da regra CSS prefers-reduced-motion no DOM
- Adaptação fluida sem rolagem horizontal entre 360px e 1920px
- Dimensão mínima de 48px x 48px para botões e ações interativas
- Anel de foco acessível (:focus-visible) de alto contraste
- Zero erros de execução ou console
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

received_reports = []

class AuditHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/report'):
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
        # Silenciar logs normais para manter a saída limpa
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
    print(" INICIANDO VERIFICAÇÃO AUTOMATIZADA - HISTÓRIA 1 (REVISÃO)")
    print("=================================================================")

    # 1. Teste estático da folha de estilos
    with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
        css_content = f.read()

    required_vars = [
        "--cor-natal-vermelho",
        "--cor-natal-verde",
        "--cor-natal-dourado",
        "--cor-neve-fundo"
    ]
    print("\n[1/4] Verificando variáveis :root e regras de acessibilidade no CSS...")
    for var in required_vars:
        if var in css_content:
            print(f"  ✓ Variável obrigatória '{var}' presente no CSS.")
        else:
            print(f"  ✗ ERRO: Variável '{var}' não encontrada!")
            sys.exit(1)

    if "@media (prefers-reduced-motion: reduce)" in css_content:
        print("  ✓ Regra @media (prefers-reduced-motion: reduce) presente no CSS.")
    else:
        print("  ✗ ERRO: Regra prefers-reduced-motion ausente!")
        sys.exit(1)

    if ":focus-visible" in css_content:
        print("  ✓ Anel de foco :focus-visible acessível presente no CSS.")
    else:
        print("  ✗ ERRO: :focus-visible ausente no CSS!")
        sys.exit(1)

    if ":not(.btn-close)" in css_content:
        print("  ✓ Seletores de botão escopados com :not(.btn-close) no CSS.")
    else:
        print("  ✗ ERRO: Seletores de botão não excluem .btn-close!")
        sys.exit(1)

    if "will-change" in css_content:
        print("  ✓ Otimização will-change para flocos de neve presente no CSS.")
    else:
        print("  ✗ ERRO: will-change ausente no CSS!")
        sys.exit(1)

    # 2. Inicializa o servidor HTTP local em porta dinâmica
    port = get_free_port()
    server = start_server(port)
    time.sleep(0.4)

    test_file_path = BASE_DIR / "test_runner.html"
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Injeção de auditoria completa no DOM
    audit_code = """
    <script>
    window.__pageErrors = [];
    window.addEventListener('error', (e) => {
        window.__pageErrors.push(e.message);
    });

    document.addEventListener('DOMContentLoaded', () => {
        const buttons = Array.from(document.querySelectorAll('button:not(.btn-close), .btn:not(.btn-close), input[type="button"]')).filter(b => !b.closest('.modal'));
        const audits = buttons.map(b => {
            const rect = b.getBoundingClientRect();
            return {
                id: b.id || b.className,
                text: b.textContent.replace(/\\s+/g, ' ').trim(),
                width: rect.width,
                height: rect.height,
                meets48px: (rect.width >= 48) && (rect.height >= 48)
            };
        });

        // Verificação dos flocos de neve no DOM
        const snowflakes = Array.from(document.querySelectorAll('.snowflake'));
        const snowflakeCount = snowflakes.length;
        let animationName = '';
        let willChange = '';
        if (snowflakeCount > 0) {
            const computedSnow = window.getComputedStyle(snowflakes[0]);
            animationName = computedSnow.animationName || '';
            willChange = computedSnow.willChange || '';
        }

        // Verificação da regra prefers-reduced-motion nas folhas de estilo carregadas
        let reducedMotionRuleFound = false;
        try {
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.media && rule.media.mediaText.includes('prefers-reduced-motion')) {
                            reducedMotionRuleFound = true;
                            break;
                        }
                    }
                } catch(e) {}
                if (reducedMotionRuleFound) break;
            }
        } catch(e) {}

        const snowContainer = document.querySelector('.snow-container');
        const snowComputed = snowContainer ? getComputedStyle(snowContainer) : null;
        const pointerEvents = snowComputed ? snowComputed.pointerEvents : '';

        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        const innerWidth = window.innerWidth;
        const innerHeight = window.innerHeight;

        const skipLink = document.querySelector('.skip-link');
        const hasSkipLink = skipLink !== null && skipLink.getAttribute('href') === '#main-content';

        const payload = {
            viewportWidth: innerWidth,
            viewportHeight: innerHeight,
            scrollWidth: scrollWidth,
            clientWidth: clientWidth,
            hasOverflow: scrollWidth > clientWidth,
            pointerEvents: pointerEvents,
            buttonAudits: audits,
            snowflakeCount: snowflakeCount,
            snowAnimationName: animationName,
            snowWillChange: willChange,
            reducedMotionRuleFound: reducedMotionRuleFound,
            hasSkipLink: hasSkipLink,
            errors: window.__pageErrors
        };

        const img = new Image();
        img.src = '/api/report?d=' + encodeURIComponent(JSON.stringify(payload));
    });
    </script>
    """

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(html_content.replace("</body>", audit_code + "\n</body>"))

    resolutions = [
        (360, 640, "Smartphone Pequeno (360px)"),
        (768, 1024, "Tablet / iPad (768px)"),
        (1920, 1080, "Desktop Full HD (1920px)")
    ]

    all_tests_passed = True
    print("\n[2/4] Executando renderização e testes no Firefox Headless...")

    try:
        for width, height, device_name in resolutions:
            print(f"\n  -> Testando em {device_name} [{width}x{height}px]...")
            screenshot_dest = ARTIFACTS_DIR / f"screen_{width}px.png"
            cmd = [
                "firefox",
                "--headless",
                f"--screenshot={screenshot_dest}",
                f"--window-size={width},{height}",
                f"http://127.0.0.1:{port}/test_runner.html"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)
            time.sleep(1)

            matching = [r for r in received_reports if abs(r['viewportWidth'] - width) <= 25]
            if not matching:
                print(f"    ✗ FALHA: Nenhum relatório recebido do navegador para {width}px")
                all_tests_passed = False
                continue

            report = matching[-1]

            # Verificação 1: Ausência de rolagem horizontal
            if report['hasOverflow']:
                print(f"    ✗ ERRO: Rolagem horizontal detectada! scrollWidth={report['scrollWidth']} > clientWidth={report['clientWidth']}")
                all_tests_passed = False
            else:
                print(f"    ✓ Sem rolagem horizontal: scrollWidth ({report['scrollWidth']}px) <= clientWidth ({report['clientWidth']}px)")

            # Verificação 2: Dimensões mínimas de 48px para botões
            for btn in report['buttonAudits']:
                if btn['meets48px']:
                    print(f"      ✓ Botão \"{btn['text']}\": {btn['width']:.1f}px x {btn['height']:.1f}px (>= 48px)")
                else:
                    print(f"      ✗ ERRO: Botão \"{btn['text']}\": {btn['width']:.1f}px x {btn['height']:.1f}px (< 48px)")
                    all_tests_passed = False

            # Verificação 3: Flocos de neve no DOM e CSS animation
            if report['snowflakeCount'] >= 10:
                print(f"    ✓ Elementos .snowflake presentes no DOM ({report['snowflakeCount']} flocos)")
            else:
                print(f"    ✗ ERRO: Poucos ou nenhum elemento .snowflake encontrado ({report['snowflakeCount']})")
                all_tests_passed = False

            if 'snowfall' in report['snowAnimationName']:
                print(f"    ✓ Animação de neve ativa nos flocos: animation-name='{report['snowAnimationName']}'")
            else:
                print(f"    ✗ ERRO: Animação de neve incorreta: '{report['snowAnimationName']}'")
                all_tests_passed = False

            # Verificação 4: Regra prefers-reduced-motion no DOM
            if report['reducedMotionRuleFound']:
                print("    ✓ Regra prefers-reduced-motion ativa e reconhecida nas folhas de estilo")
            else:
                print("    ✗ ERRO: Regra prefers-reduced-motion não encontrada nas regras CSS carregadas")
                all_tests_passed = False

            # Verificação 5: Pointer-events do container de neve
            if report['pointerEvents'] == 'none':
                print("    ✓ Container de neve com pointer-events: none garantido")
            else:
                print(f"    ✗ ERRO: pointer-events é '{report['pointerEvents']}'")
                all_tests_passed = False

            # Verificação 6: Skip link acessível
            if report['hasSkipLink']:
                print("    ✓ Skip-link acessível presente e apontando para #main-content")
            else:
                print("    ✗ ERRO: Skip-link ausente ou inválido")
                all_tests_passed = False

            # Verificação 7: Erros de console
            if not report['errors']:
                print("    ✓ Zero erros no console JavaScript")
            else:
                print(f"    ✗ ERRO: Erros de console: {report['errors']}")
                all_tests_passed = False

    finally:
        if test_file_path.exists():
            test_file_path.unlink()
        server.shutdown()
        server.server_close()

    print("\n=================================================================")
    if all_tests_passed:
        print(" RESULTADO: TODOS OS CRITÉRIOS DE ACEITAÇÃO PASSARAM COM SUCESSO! 🎉")
        print("=================================================================")
        sys.exit(0)
    else:
        print(" RESULTADO: ALGUNS CRITÉRIOS FALHARAM ❌")
        print("=================================================================")
        sys.exit(1)

if __name__ == '__main__':
    main()
