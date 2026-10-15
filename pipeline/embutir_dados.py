"""
RASTRE.IA - embute o pacote do pipeline no protótipo

O protótipo (app/mvpN.html) é um arquivo HTML único que lê os dados do bloco
<script id="rm-data" type="application/json">. Este script substitui esse bloco pelo
rastreia_data.json gerado por preparar_dados.py, fechando o ciclo pipeline -> tela.

Uso:
    python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json --saida app/mvp5.html
    python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json --verificar
"""
import argparse, json, re

INI = '<script id="rm-data" type="application/json">'
FIM = "</script>"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True); ap.add_argument("--dados", required=True)
    ap.add_argument("--saida"); ap.add_argument("--verificar", action="store_true", help="só compara o bloco embutido com o JSON")
    a = ap.parse_args()
    html = open(a.html, encoding="utf-8").read()
    i = html.find(INI); assert i >= 0, "bloco rm-data não encontrado"
    j = html.find(FIM, i + len(INI))
    atual = json.loads(html[i + len(INI):j])
    novo = json.load(open(a.dados, encoding="utf-8"))
    if a.verificar:
        print("iguais" if atual == novo else "DIFERENTES"); return
    blob = json.dumps(novo, ensure_ascii=False, separators=(",", ":"))
    open(a.saida or a.html, "w", encoding="utf-8").write(html[:i + len(INI)] + blob + html[j:])
    print(f"embutido {len(blob)} bytes em {a.saida or a.html}")

if __name__ == "__main__":
    main()
