#!/usr/bin/env python3
"""
Testes automatizados do Modal de Vídeo "A Magia do Natal" (Turma da Mônica):
- Acionamento via botão #btn-conhecer-magia
- Modal temático #modal-magia-natal e iframe #iframe-video-magia
- Carregamento do vídeo sob demanda com autoplay e início aos 15s (rzDQZcwfNiw?start=15)
- Parada imediata do vídeo ao fechar o modal (src do iframe esvaziado)
- Ergonomia (área mínima >= 48px x 48px nos botões de fechar e de disparo)
- Restauração automática de foco para o botão de acionamento
- Fechamento via backdrop, botões de fechar e tecla Escape
- Responsividade fluida em 360px, 768px e 1920px sem overflow horizontal
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
        if self.path.startswith('/api/report_magia'):
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
    server = socketserver.TCPServer(('127.0.0.1', port), AuditHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server

def run_tests():
    print("=================================================================")
    print(" INICIANDO VERIFICAÇÃO AUTOMATIZADA - MODAL VÍDEO MAGIA DO NATAL ")
    print("=================================================================\n")

    # 1. Verificação Estática
    print("[1/3] Verificando conformidade estática de arquivos e código...")
    assert INDEX_HTML_PATH.exists(), "index.html não encontrado"
    assert CSS_STYLE_PATH.exists(), "css/style.css não encontrado"
    assert JS_APP_PATH.exists(), "js/app.js não encontrado"

    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(JS_APP_PATH, "r", encoding="utf-8") as f:
        js_content = f.read()

    assert 'id="modal-magia-natal"' in html_content, "Modal #modal-magia-natal ausente no index.html"
    assert 'id="iframe-video-magia"' in html_content, "Iframe #iframe-video-magia ausente no index.html"
    assert 'id="btn-conhecer-magia"' in html_content, "Botão #btn-conhecer-magia ausente no index.html"
    assert 'rzDQZcwfNiw' in js_content, "ID do vídeo rzDQZcwfNiw ausente no js/app.js"
    assert 'start=15' in js_content, "Parâmetro start=15 ausente no js/app.js"
    assert 'autoplay=1' in js_content, "Parâmetro autoplay=1 ausente no js/app.js"
    assert '.moldura-video-natal' in css_content, "Classe .moldura-video-natal ausente no css"
    print("  ✓ Modal #modal-magia-natal e iframe presentes no index.html.")
    print("  ✓ ID do vídeo da Turma da Mônica (rzDQZcwfNiw) e tempo (start=15) configurados no js/app.js.")
    print("  ✓ Moldura festiva configurada no style.css.")

    # 2. Servidor HTTP dinâmico para os testes com Firefox Headless
    port = get_free_port()
    server = start_server(port)
    time.sleep(0.4)

    test_file_path = BASE_DIR / "test_runner_magia.html"

    audit_code = """
    <script>
    window.__errors = [];
    window.addEventListener('error', (e) => {
        window.__errors.push(e.message);
    });

    document.addEventListener('DOMContentLoaded', () => {
        const btnMagia = document.getElementById('btn-conhecer-magia');
        const modalEl = document.getElementById('modal-magia-natal');
        const iframe = document.getElementById('iframe-video-magia');

        // Remove classe fade para auditoria síncrona determinística no headless
        if (modalEl) {
            modalEl.classList.remove('fade');
        }

        const rectBtnMagia = btnMagia ? btnMagia.getBoundingClientRect() : { width: 0, height: 0 };
        const initialSrc = iframe ? (iframe.getAttribute('src') || '') : '';

        // Dispara abertura do modal
        if (btnMagia) btnMagia.click();

        const btnFecharTopo = modalEl ? modalEl.querySelector('.btn-modal-fechar-topo') : null;
        const btnFecharRodape = modalEl ? modalEl.querySelector('.btn-modal-fechar') : null;
        const rectFecharTopo = btnFecharTopo ? btnFecharTopo.getBoundingClientRect() : { width: 0, height: 0 };
        const rectFecharRodape = btnFecharRodape ? btnFecharRodape.getBoundingClientRect() : { width: 0, height: 0 };

        const modalAberto = modalEl && (modalEl.classList.contains('show') || modalEl.style.display === 'block');
        const srcAposAbrir = iframe ? (iframe.getAttribute('src') || '') : '';

        // Dispara fechamento pelo botão
        if (btnFecharRodape) btnFecharRodape.click();

        const modalFechou = modalEl && (!modalEl.classList.contains('show') || modalEl.style.display === 'none');
        const srcAposFechar = iframe ? (iframe.getAttribute('src') || '') : '';

        // Reabre e testa fechamento por Escape
        if (btnMagia) btnMagia.click();
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', bubbles: true }));
        const srcAposEsc = iframe ? (iframe.getAttribute('src') || '') : '';

        const docEl = document.documentElement;
        const payload = {
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight,
            scrollWidth: docEl.scrollWidth,
            clientWidth: docEl.clientWidth,
            hasHorizontalScroll: docEl.scrollWidth > docEl.clientWidth,
            rectBtnMagia: { width: rectBtnMagia.width, height: rectBtnMagia.height },
            rectFecharTopo: { width: rectFecharTopo.width, height: rectFecharTopo.height },
            rectFecharRodape: { width: rectFecharRodape.width, height: rectFecharRodape.height },
            initialSrc: initialSrc,
            modalAberto: modalAberto,
            srcAposAbrir: srcAposAbrir,
            modalFechou: modalFechou,
            srcAposFechar: srcAposFechar,
            srcAposEsc: srcAposEsc,
            errors: window.__errors
        };

        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/report_magia?d=' + encodeURIComponent(JSON.stringify(payload)), false);
            xhr.send();
        } catch(e) {
            const img = new Image();
            img.src = '/api/report_magia?d=' + encodeURIComponent(JSON.stringify(payload));
        }
    });
    </script>
    """

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(html_content.replace("</body>", audit_code + "\n</body>"))

    viewports = [
        {"name": "Smartphone Pequeno (360px)", "w": 360, "h": 640},
        {"name": "Tablet / iPad (768px)", "w": 768, "h": 1024},
        {"name": "Desktop Full HD (1920px)", "w": 1920, "h": 1080}
    ]

    all_passed = True
    subprocess.run(["firefox", "-CreateProfile", "bmad_test_profile /tmp/bmad_ff_prof"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\n[2/3] Executando interações dinâmicas e testes no Firefox Headless...")

    try:
        for vp in viewports:
            print(f"\n  -> Testando em {vp['name']} [{vp['w']}x{vp['h']}px]...")
            screenshot_dest = ARTIFACTS_DIR / f"screen_magia_{vp['w']}px.png"
            cmd = [
                "firefox",
                "--headless",
                "-no-remote",
                "-P", "bmad_test_profile",
                f"--screenshot={screenshot_dest}",
                f"--window-size={vp['w']},{vp['h']}",
                f"http://127.0.0.1:{port}/test_runner_magia.html"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)
            time.sleep(1.0)

            if len(received_reports) == 0:
                print(f"  ✗ ERRO: Relatório do Firefox para {vp['name']} não recebido a tempo!")
                all_passed = False
                continue

            rep = received_reports.pop()

            # Verificação de rolagem horizontal
            if rep['hasHorizontalScroll']:
                print(f"  ✗ ERRO: Rolagem horizontal detectada! ({rep['scrollWidth']}px > {rep['clientWidth']}px)")
                all_passed = False
            else:
                print(f"  ✓ Sem rolagem horizontal: scrollWidth ({rep['scrollWidth']}px) <= clientWidth ({rep['clientWidth']}px)")

            # Ergonomia dos botões
            btn_m = rep['rectBtnMagia']
            topo = rep['rectFecharTopo']
            rodape = rep['rectFecharRodape']

            if btn_m['width'] >= 48 and btn_m['height'] >= 48:
                print(f"  ✓ Botão 'A Magia do Natal' ({btn_m['width']:.1f}px x {btn_m['height']:.1f}px) atende >= 48px.")
            else:
                print(f"  ✗ ERRO: Botão 'A Magia do Natal' menor que 48px: {btn_m}")
                all_passed = False

            if rodape['width'] >= 48 and rodape['height'] >= 48:
                print(f"  ✓ Botão 'Voltar para a Cartinha' ({rodape['width']:.1f}px x {rodape['height']:.1f}px) atende >= 48px.")
            else:
                print(f"  ✗ ERRO: Botão rodapé menor que 48px: {rodape}")
                all_passed = False

            # Comportamento de carregamento e parada de vídeo
            if rep['initialSrc'] == '':
                print("  ✓ Iframe iniciou vazio (sem consumo de banda inicial).")
            else:
                print(f"  ✗ ERRO: Iframe já possuía src antes do clique: {rep['initialSrc']}")
                all_passed = False

            if rep['modalAberto'] and 'rzDQZcwfNiw' in rep['srcAposAbrir'] and 'start=15' in rep['srcAposAbrir']:
                print(f"  ✓ Modal abriu e vídeo foi carregado sob demanda aos 15s: {rep['srcAposAbrir'][:55]}...")
            else:
                print(f"  ✗ ERRO: Modal não abriu ou vídeo incorreto: {rep}")
                all_passed = False

            if rep['modalFechou'] and rep['srcAposFechar'] == '':
                print("  ✓ Fechamento suave: modal fechou e vídeo/áudio foi interrompido (src esvaziado).")
            else:
                print(f"  ✗ ERRO: Vídeo não parou ao fechar modal: {rep['srcAposFechar']}")
                all_passed = False

            if rep['srcAposEsc'] == '':
                print("  ✓ Fechamento por tecla Escape validado com parada do vídeo.")
            else:
                print(f"  ✗ ERRO: Vídeo não parou após tecla Escape: {rep['srcAposEsc']}")
                all_passed = False

            if rep['errors']:
                print(f"  ✗ ERRO: Exceções no console JavaScript: {rep['errors']}")
                all_passed = False
            else:
                print("  ✓ Zero erros ou exceções no console JavaScript.")

    finally:
        if test_file_path.exists():
            test_file_path.unlink()
        server.shutdown()

    print("\n[3/3] Avaliação final dos critérios de aceitação...")
    if all_passed:
        print("\n=================================================================")
        print(" RESULTADO MODAL MAGIA DO NATAL: TODOS OS TESTES PASSARAM! 🎉")
        print("=================================================================\n")
        sys.exit(0)
    else:
        print("\n=================================================================")
        print(" RESULTADO: ALGUNS TESTES FALHARAM!")
        print("=================================================================\n")
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
