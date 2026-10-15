"""
RASTRE.IA - perfilamento da base e análise exploratória

Gera, a partir dos CSVs crus (data/entrada) e das saídas do pipeline (data/saida):
    docs/perfilamento-base.md      volume, tipos, chaves, integridade, completude, contagem antes/depois,
                                   registro dos tratamentos (do qualidade_dados.json) e medidas de dispersão
    docs/figuras/*.png             histograma, boxplot e dispersão sobre a base comum

Uso (depois de rodar preparar_dados.py):
    python pipeline/perfilar_base.py --entrada data/entrada --saida data/saida --docs docs
"""
import argparse, json, os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TABELAS = {"equipes": "equipes.csv", "resultados_ciclos": "resultados_ciclos.csv", "eixo3_indicadores": "eixo3_indicadores.csv",
           "nps_atributos": "nps_atributos.csv", "planos_acao": "planos_acao.csv"}
CHAVES = {"equipes": ["codigo_ine"], "resultados_ciclos": ["codigo_ine", "ciclo"], "eixo3_indicadores": ["codigo_ine", "ciclo", "codigo_indicador"],
          "nps_atributos": ["codigo_ine", "ciclo", "codigo_atributo"], "planos_acao": ["id_plano"]}
COR = "#2F5D8A"

def md_table(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True); ap.add_argument("--saida", required=True); ap.add_argument("--docs", required=True)
    a = ap.parse_args()
    fig_dir = os.path.join(a.docs, "figuras"); os.makedirs(fig_dir, exist_ok=True)
    cru = {n: pd.read_csv(os.path.join(a.entrada, f), dtype=str) for n, f in TABELAS.items()}
    limpo = {n: pd.read_csv(os.path.join(a.saida, "limpo", f), dtype=str) for n, f in TABELAS.items()}
    log = json.load(open(os.path.join(a.saida, "qualidade_dados.json"), encoding="utf-8"))
    S = []

    S.append("# Perfilamento da base sintética do Recife Monitora\n")
    S.append("Gerado por `pipeline/perfilar_base.py`. Base 100% sintética (DADOS SIMULADOS).\n")

    # 1. volume e contagem antes/depois
    S.append("## 1. Volume e contagem antes e depois da limpeza\n")
    vol = pd.DataFrame([{"tabela": n, "grão": "/".join(CHAVES[n]), "linhas cruas": len(cru[n]), "linhas após limpeza": len(limpo[n]),
                         "removidas": len(cru[n]) - len(limpo[n]), "colunas": len(cru[n].columns)} for n in TABELAS])
    S.append(md_table(vol) + "\n")

    # 2. tipos e completude por coluna (base crua)
    S.append("## 2. Tipos, completude e domínio por coluna (base crua)\n")
    for n, df in cru.items():
        rows = []
        for c in df.columns:
            s = df[c]
            numv = pd.to_numeric(s.astype(str).str.replace(",", ".", regex=False), errors="coerce")
            tipo = "numérico" if numv.notna().sum() >= 0.9 * s.notna().sum() and s.notna().sum() > 0 else "texto/categórico"
            rows.append({"coluna": c, "tipo inferido": tipo, "nulos": int(s.isna().sum()), "completude": f"{100 * s.notna().mean():.1f}%",
                         "valores distintos": int(s.nunique()), "exemplo": str(s.dropna().iloc[0])[:30] if s.notna().any() else ""})
        S.append(f"### {n}.csv\n\n" + md_table(pd.DataFrame(rows)) + "\n")

    # 3. chaves e integridade referencial
    S.append("## 3. Chaves e integridade referencial\n")
    rows = []
    ines = set(cru["equipes"].codigo_ine)
    for n, k in CHAVES.items():
        df = cru[n]; dup = int(df.duplicated(k).sum())
        orf = int((~df.codigo_ine.isin(ines)).sum()) if "codigo_ine" in df.columns and n != "equipes" else 0
        rows.append({"tabela": n, "chave": "+".join(k), "duplicatas na chave (cru)": dup, "codigo_ine sem cadastro (cru)": orf,
                     "duplicatas após limpeza": int(limpo[n].duplicated(k).sum())})
    S.append(md_table(pd.DataFrame(rows)) + "\n")

    # 4. registro dos tratamentos
    S.append("## 4. Registro de cada tratamento (qualidade_dados.json)\n")
    S.append("Contagem = linhas afetadas antes do tratamento; a contagem total após limpeza está na seção 1.\n")
    S.append(md_table(pd.DataFrame([{"#": i + 1, "tabela": l["tabela"], "problema": l["problema"], "linhas": l["linhas"], "decisão": l["decisao"]}
                                    for i, l in enumerate(log)])) + "\n")

    # 5. medidas de dispersão (base limpa, pontuação final por ciclo)
    S.append("## 5. Medidas de dispersão da pontuação final (base limpa, equipes pontuadas)\n")
    rc = limpo["resultados_ciclos"].copy()
    rc["pf"] = pd.to_numeric(rc.pontuacao_final, errors="coerce")
    rc = rc[rc.pf.notna()]
    disp = rc.groupby("ciclo").pf.agg(n="count", media="mean", mediana="median", desvio="std", minimo="min", q1=lambda x: x.quantile(.25),
                                     q3=lambda x: x.quantile(.75), maximo="max").round(1).reset_index()
    S.append(md_table(disp) + "\n")
    ult = disp.iloc[-1]
    S.append(f"Observações: no ciclo {ult.ciclo}, a mediana ({ult.mediana}) fica próxima da média ({ult.media}), sem assimetria forte; "
             f"o desvio padrão de {ult.desvio} pontos sobre uma escala de 1.000 indica dispersão moderada entre equipes; "
             f"o intervalo interquartil ({ult.q1} a {ult.q3}) concentra metade das equipes na zona de Aperfeiçoamento.\n")
    eq = limpo["equipes"].copy(); eq["prof"] = pd.to_numeric(eq.n_profissionais, errors="coerce")
    u = rc[rc.ciclo == ult.ciclo].merge(eq[["codigo_ine", "distrito_sanitario", "grupo", "prof"]], on="codigo_ine")
    S.append("Por distrito sanitário (último ciclo):\n")
    S.append(md_table(u.groupby("distrito_sanitario").pf.agg(n="count", media="mean", mediana="median", desvio="std").round(1).reset_index()) + "\n")
    corr = u[["pf", "prof"]].corr().iloc[0, 1]
    S.append(f"Correlação entre pontuação final e número de profissionais no último ciclo: r = {corr:.2f} "
             f"({'fraca' if abs(corr) < 0.3 else 'moderada' if abs(corr) < 0.6 else 'forte'}); o porte não explica a pontuação, "
             "o que sustenta a normalização por porte apenas para alertas, não para o ranking.\n")

    # 6. figuras
    S.append("## 6. Figuras\n")
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(u.pf, bins=20, color=COR, alpha=.9)
    for v, nome in ((900, "Excelência"), (800, "Qualidade"), (600, "Aperfeiçoamento"), (400, "Crítica")):
        ax.axvline(v, color="#999", ls="--", lw=.8); ax.text(v, ax.get_ylim()[1] * .95, nome, rotation=90, va="top", ha="right", fontsize=8, color="#666")
    ax.set_title(f"Distribuição da pontuação final, ciclo {ult.ciclo} (DADOS SIMULADOS)"); ax.set_xlabel("pontuação final (0 a 1.000)"); ax.set_ylabel("equipes")
    fig.tight_layout(); fig.savefig(os.path.join(fig_dir, "hist_pontuacao_final.png"), dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ds = sorted(u.distrito_sanitario.unique(), key=lambda s: ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"].index(s.replace("DS ", "")))
    ax.boxplot([u[u.distrito_sanitario == d].pf for d in ds], tick_labels=ds, patch_artist=True,
               boxprops=dict(facecolor=COR, alpha=.5), medianprops=dict(color="#222"))
    ax.set_title(f"Pontuação final por distrito sanitário, ciclo {ult.ciclo} (DADOS SIMULADOS)"); ax.set_ylabel("pontuação final")
    fig.tight_layout(); fig.savefig(os.path.join(fig_dir, "boxplot_distrito.png"), dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    e1 = pd.to_numeric(u.eixo1_total, errors="coerce"); e3 = pd.to_numeric(u.eixo3_total, errors="coerce")
    ax.scatter(e1, e3, s=18, color=COR, alpha=.7)
    ax.set_title(f"Eixo 1 (autoavaliação) x Eixo 3 (desempenho), ciclo {ult.ciclo} (DADOS SIMULADOS)")
    ax.set_xlabel("Eixo 1 (0 a 200)"); ax.set_ylabel("Eixo 3 (0 a 600)")
    fig.tight_layout(); fig.savefig(os.path.join(fig_dir, "dispersao_eixo1_eixo3.png"), dpi=150); plt.close(fig)
    r13 = pd.concat([e1, e3], axis=1).corr().iloc[0, 1]
    S.append(f"- `figuras/hist_pontuacao_final.png`: histograma da pontuação final no ciclo {ult.ciclo} com as faixas de zona do Manual.\n"
             f"- `figuras/boxplot_distrito.png`: boxplot por distrito sanitário.\n"
             f"- `figuras/dispersao_eixo1_eixo3.png`: dispersão Eixo 1 x Eixo 3 (r = {r13:.2f}).\n")

    with open(os.path.join(a.docs, "perfilamento-base.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(S))
    print(f"perfilamento escrito em {os.path.join(a.docs, 'perfilamento-base.md')}; figuras em {fig_dir}")

if __name__ == "__main__":
    main()
