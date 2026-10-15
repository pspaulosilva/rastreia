"""
RASTRE.IA - verificação dos números do Protótipo 5 contra a base comum

Responde ao "Primeiro ponto a esclarecer" da devolutiva do SR1: o Protótipo 5 mostra
Encruzilhada I = 422, Curado III = 392, média da rede = 681 e 27 equipes abaixo de 600,
enquanto a base crua tem 405 e 373,8 para as mesmas equipes.

Este script reproduz os dois cálculos lado a lado:
  - "cru": pontuacao_final como veio na base (blocos do Eixo 1 com máximos A80/B60/C60);
  - "realinhado": pontuacao_final recomposta pelo pipeline v1.1 (preparar_dados.py), que
    reescala os blocos do Eixo 1 para os máximos do Manual de Avaliação (A40/B80/C80).

Uso (depois de rodar preparar_dados.py):
    python pipeline/verificar_prototipo5.py --entrada data/entrada --saida data/saida
"""
import argparse, json, os, re
import pandas as pd
import numpy as np

def norm_ciclo(c):
    c = str(c).strip()
    m = re.match(r"^(\d{4})[.\-Q](\d)$", c)
    if m: return f"{m.group(1)}.{m.group(2)}"
    m = re.match(r"^(\d)/(\d{4})$", c)
    return f"{m.group(2)}.{m.group(1)}" if m else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--entrada", required=True); ap.add_argument("--saida", required=True); a = ap.parse_args()
    pac = json.load(open(os.path.join(a.saida, "rastreia_data.json"), encoding="utf-8"))
    raw = pd.read_csv(os.path.join(a.entrada, "resultados_ciclos.csv"), dtype=str)
    raw["ciclo"] = raw.ciclo.map(norm_ciclo)
    num = lambda s: pd.to_numeric(s.astype(str).str.replace(",", ".", regex=False), errors="coerce")
    for c in ["pontuacao_final", "eixo1_bloco_a", "eixo1_bloco_b", "eixo1_bloco_c", "eixo1_total", "eixo2_total", "eixo3_total"]:
        raw[c] = num(raw[c])

    por_nome = {t["nome"]: t for t in pac["equipes"]}
    print("ciclo 2026.2 | equipe | base crua | realinhado (pipeline v1.1) | Protótipo 5")
    for nome, p5 in (("eSF Encruzilhada I", 422), ("eSF Curado III", 392)):
        t = por_nome[nome]; ine = t["ine"]
        cru = raw[(raw.codigo_ine == ine) & (raw.ciclo == "2026.2")].iloc[0]
        rea = t["res"]["2026.2"]
        print(f"{nome:20s} | cru {cru.pontuacao_final:6.1f} (A {cru.eixo1_bloco_a} B {cru.eixo1_bloco_b} C {cru.eixo1_bloco_c}) | "
              f"realinhado {rea['f']:6.1f} (A {rea['a']} B {rea['b']} C {rea['c']}) | P5 {p5}")

    f = [t["res"]["2026.2"]["f"] for t in pac["equipes"] if t["res"].get("2026.2", {}).get("f") is not None]
    c = raw[(raw.ciclo == "2026.2") & raw.pontuacao_final.between(0, 1000)]
    print(f"rede 2026.2 crua:        n={len(c):3d} media={c.pontuacao_final.mean():6.1f} abaixo de 600={int((c.pontuacao_final < 600).sum())}")
    print(f"rede 2026.2 realinhada:  n={len(f):3d} media={np.mean(f):6.1f} abaixo de 600={sum(v < 600 for v in f)}   (Protótipo 5: media 681, 27 abaixo de 600)")

if __name__ == "__main__":
    main()
