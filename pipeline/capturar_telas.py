"""
RASTRE.IA - captura de telas dos protótipos com Chromium (Playwright)

Abre cada protótipo em app/mvpN.html, navega até a tela indicada (botão data-v)
e salva a captura em docs/capturas/. Uso:
    pip install playwright && playwright install chromium
    python pipeline/capturar_telas.py --tela qualidade --prototipos 6
"""
import argparse, os
from playwright.sync_api import sync_playwright

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tela", default="qualidade"); ap.add_argument("--prototipos", nargs="+", default=["6"])
    ap.add_argument("--app", default="app"); ap.add_argument("--sufixo", default="", help="ex.: --sufixo=-dicionario"); ap.add_argument("--query", default="", help="ex.: ?faixas=dicionario"); ap.add_argument("--saida", default=os.path.join("docs", "capturas"))
    a = ap.parse_args(); os.makedirs(a.saida, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for n in a.prototipos:
            pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
            pg.goto("file://" + os.path.abspath(os.path.join(a.app, f"mvp{n}.html")) + a.query); pg.wait_for_timeout(800)
            pg.click(f'#nav button[data-v="{a.tela}"]'); pg.wait_for_timeout(800)
            out = os.path.join(a.saida, f"prototipo{n}-{a.tela}{a.sufixo}.png")
            pg.screenshot(path=out, full_page=True); print("salvo", out); pg.close()
        b.close()

if __name__ == "__main__":
    main()
