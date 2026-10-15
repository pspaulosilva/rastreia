"""
RASTRE.IA - verificação dos números do Protótipo 5 contra a base comum

Responde ao "Primeiro ponto a esclarecer" da devolutiva do SR1: o Protótipo 5 mostra
Encruzilhada I = 422, Curado III = 392, média da rede = 681 e 27 equipes abaixo de 600,
enquanto a base tem 405 e 373,8 para as mesmas equipes.

Compara, equipe a equipe, os dois pacotes do mesmo pipeline:
  - "base" (--modo dicionario, v1.0): a base comum como veio, blocos do Eixo 1 com máximos
    A80/B60/C60; é o pacote dos Protótipos 3 e 4, que o professor conferiu número a número;
  - "P5" (--modo manual, v1.1): blocos reescalados para os máximos do Manual de Avaliação
    (A40/B80/C80) e pontuação final recomposta; é o pacote embutido no Protótipo 5.

Mostra que toda a diferença vem do reescalonamento: P5 = base + (A x 40/80 - A) + (B x 80/60 - B)
+ (C x 80/60 - C), com Eixos 2 e 3 iguais, em todas as equipes e ciclos.

Uso:
    python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida
    python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida-dicionario --modo dicionario
    python pipeline/verificar_prototipo5.py --base data/saida-dicionario --p5 data/saida [--md docs/verificacao-prototipo-5.md]
"""
import argparse, json, os

# equipes dos alertas críticos do Protótipo 5 (perfil central, ciclo 2026.2), na ordem da tela
ALERTAS_P5 = ["6000000098", "6000000032", "6000000049", "6000000079", "6000000097", "6000000048",
              "6000000017", "6000000035", "6000000099", "6000000082", "6000000090", "6000000129"]
CICLO = "2026.2"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="saída do pipeline com --modo dicionario")
    ap.add_argument("--p5", required=True, help="saída do pipeline com --modo manual (padrão)")
    ap.add_argument("--md", help="grava o relatório em Markdown neste arquivo")
    a = ap.parse_args()
    base = json.load(open(os.path.join(a.base, "rastreia_data.json"), encoding="utf-8"))
    p5 = json.load(open(os.path.join(a.p5, "rastreia_data.json"), encoding="utf-8"))
    bb, bm = base["meta"]["blocos"], p5["meta"]["blocos"]
    B = {t["ine"]: t for t in base["equipes"]}
    out = []

    # 1. identidade das equipes: mesmo INE, profissionais e grupo; só o rótulo muda
    out.append(f"## 1. Equipes dos alertas críticos do Protótipo 5 (ciclo {CICLO})\n")
    out.append("| INE | Nome no Protótipo 5 | Rótulo na base | Grupo | Prof. | Base (A + B + C + E2 + E3) | P5 (A + B + C + E2 + E3) | Na tela do P5 |")
    out.append("|---|---|---|---|---|---|---|---|")
    for t in sorted((t for t in p5["equipes"] if t["ine"] in ALERTAS_P5), key=lambda t: ALERTAS_P5.index(t["ine"])):
        b = B[t["ine"]]; x, y = b["res"][CICLO], t["res"][CICLO]
        assert (b["grupo"], b["prof"]) == (t["grupo"], t["prof"])
        fmt = lambda r: f"{r['f']:.1f} = {r['a']} + {r['b']} + {r['c']} + {r['e2']} + {r['e3']}".replace(".", ",")
        out.append(f"| {t['ine']} | {t['nome']} | {b['nome']} | {t['grupo']} | {t['prof']} | {fmt(x)} | {fmt(y)} | {round(y['f'])} |")

    # 2. todas as equipes e ciclos: a diferença é exatamente o reescalonamento dos blocos
    n = ok = 0; maxerr = 0.0
    for t in p5["equipes"]:
        for c, y in t["res"].items():
            if y.get("d"): continue
            x = B[t["ine"]]["res"][c]; n += 1
            # cada bloco reescalado é arredondado a 1 casa (tolerância 0,05) e a soma acumula até 0,15
            perto = lambda v, ref: v is None and ref is None or (v is not None and ref is not None and abs(v - ref) <= 0.05 + 1e-6)
            ra = None if x["a"] is None else x["a"] * bm["a"] / bb["a"]
            blocos = perto(y["a"], ra) and perto(y["b"], x["b"] * bm["b"] / bb["b"]) and perto(y["c"], x["c"] * bm["c"] / bb["c"])
            err = abs(y["f"] - ((y["a"] or 0) + y["b"] + y["c"] + x["e2"] + x["e3"])); maxerr = max(maxerr, abs(y["f"] - x["f"] - ((y["a"] or 0) - (x["a"] or 0) + y["b"] - x["b"] + y["c"] - x["c"])))
            ok += blocos and y["e2"] == x["e2"] and y["e3"] == x["e3"] and err <= 0.15
    out.append(f"\n## 2. Todas as equipes e ciclos\n\n{ok} de {n} linhas pontuadas (132 equipes, 11 ciclos) têm P5 = base com blocos reescalados "
               f"(A x {bm['a']}/{bb['a']}, B x {bm['b']}/{bb['b']}, C x {bm['c']}/{bb['c']}) e Eixos 2 e 3 idênticos; "
               f"fora a variação dos blocos, a pontuação final difere no máximo {f'{maxerr:.1f}'.replace('.', ',')} ponto, só de arredondamento.")

    # 3. rede: mesmas 129 equipes pontuadas nos dois pacotes
    fb = [t["res"][CICLO]["f"] for t in base["equipes"] if t["res"].get(CICLO, {}).get("f") is not None]
    fp = [t["res"][CICLO]["f"] for t in p5["equipes"] if t["res"].get(CICLO, {}).get("f") is not None]
    out.append(f"\n## 3. Rede em {CICLO} (equipes pontuadas, sem os 13 INEs sem cadastro)\n")
    out.append("| Medida | Base (Protótipos 3 e 4) | P5 realinhado | Na tela do P5 |\n|---|---|---|---|")
    out.append(f"| Equipes pontuadas | {len(fb)} | {len(fp)} | 129 |")
    out.append(f"| Média da rede | {sum(fb)/len(fb):.1f} | {sum(fp)/len(fp):.1f} | 681 |".replace(".", ","))
    out.append(f"| Abaixo de 600 | {sum(v < 600 for v in fb)} | {sum(v < 600 for v in fp)} | 27 |")
    txt = "\n".join(out)
    print(txt)
    if a.md: open(a.md, "w", encoding="utf-8").write("# Verificação do Protótipo 5 (gerado por pipeline/verificar_prototipo5.py)\n\nDADOS SIMULADOS.\n\n" + txt + "\n")

if __name__ == "__main__":
    main()
