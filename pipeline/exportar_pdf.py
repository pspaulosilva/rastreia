"""
RASTRE.IA - exporta documentos Markdown para PDF (Chromium via Playwright)

Gera um PDF por arquivo .md da pasta indicada, em A4 paisagem (as tabelas de backlog e
riscos são largas), com rodapé de página. Uso:
    pip install markdown playwright && playwright install chromium
    python pipeline/exportar_pdf.py --pasta docs/processo --saida docs/processo/pdf
"""
import argparse, glob, html, os
import markdown
from playwright.sync_api import sync_playwright

CSS = """
@page{size:A4 landscape;margin:16mm 14mm 18mm}
body{font:10.5pt/1.5 -apple-system,"Helvetica Neue",Arial,sans-serif;color:#1d2040}
h1{font-size:20pt;font-weight:400;color:#5b7cfa;margin:0 0 6pt}
h2{font-size:13pt;color:#2d2fa6;margin:16pt 0 6pt;border-bottom:1px solid #dadded;padding-bottom:3pt}
h3{font-size:11pt;margin:12pt 0 4pt}
p,li{max-width:95ch}
table{border-collapse:collapse;width:100%;margin:6pt 0 10pt;font-size:8.8pt;page-break-inside:auto}
tr{page-break-inside:avoid}
th{background:#5b7cfa;color:#fff;text-align:left;font-weight:600;padding:5pt 6pt}
td{border-bottom:1px solid #dadded;padding:4pt 6pt;vertical-align:top}
tr:nth-child(even) td{background:#f3f4fb}
code{font:8.5pt Menlo,monospace;background:#eef0f8;padding:1px 4px;border-radius:3px}
.marca{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#7d82a2;margin-bottom:10pt}
"""
RODAPE = ('<div style="font:7.5pt Arial,sans-serif;color:#7d82a2;width:100%;padding:0 14mm;display:flex;justify-content:space-between">'
          '<span>RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2</span>'
          '<span>{arquivo} · página <span class="pageNumber"></span> de <span class="totalPages"></span></span></div>')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", default=os.path.join("docs", "processo"))
    ap.add_argument("--saida", default=os.path.join("docs", "processo", "pdf"))
    a = ap.parse_args(); os.makedirs(a.saida, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for md in sorted(glob.glob(os.path.join(a.pasta, "*.md"))):
            nome = os.path.splitext(os.path.basename(md))[0]
            corpo = markdown.markdown(open(md, encoding="utf-8").read(), extensions=["tables", "sane_lists"])
            pg.set_content(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(nome)}</title>'
                           f'<style>{CSS}</style></head><body><div class="marca">RASTRE.IA · Recife Monitora · Processo</div>{corpo}</body></html>')
            out = os.path.join(a.saida, f"{nome}.pdf")
            pg.pdf(path=out, format="A4", landscape=True, print_background=True, display_header_footer=True,
                   header_template="<span></span>", footer_template=RODAPE.format(arquivo=html.escape(os.path.basename(md))),
                   margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
            print("salvo", out)
        b.close()

if __name__ == "__main__":
    main()
