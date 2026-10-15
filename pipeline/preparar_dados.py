"""
RASTRE.IA - pipeline de preparação da base sintética do Recife Monitora
Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2

Uso:
    python preparar_dados.py --entrada <pasta com os 5 CSVs> --saida <pasta de saída> [--modo manual|dicionario]
    python preparar_dados.py --entrada <pasta com os 5 CSVs> --saida <pasta de saída> --pacote v6

Modos (parâmetros do programa, ver PARAMETROS):
    manual      (padrão, v1.1) blocos do Eixo 1 reescalados para A40/B80/C80 e zonas 900/800/600/400
                (Manual de Avaliação); nomes fictícios de bairros. Gera o pacote do Protótipo 5.
    dicionario  (v1.0) base como veio: blocos A80/B60/C60 e zonas 850/700/550/400 (dicionário da
                base); nomes sintéticos originais. Gera o pacote dos Protótipos 3 e 4.

Saídas:
    <saida>/limpo/*.csv            tabelas tratadas (mesmo grão da origem)
    <saida>/qualidade_dados.json   log estruturado de cada problema encontrado e decisão tomada
    <saida>/rastreia_data.json     pacote compacto consumido pelos Protótipos 3 a 5 (dados embutidos)
    <saida>/rastreia_data_v6.json  com --pacote v6: os dois modos, contagem antes/depois de cada
                                   tratamento e perfilamento da base; consumido pelo Protótipo 6

Princípio: a ORIGEM dos dados fica isolada nesta função `carregar()`. Quando o middleware
de leitura do cliente estiver disponível, apenas essa função muda.

Base 100% sintética. Nenhum valor corresponde a equipes ou resultados reais.
"""
import argparse, json, re, os
import pandas as pd
import numpy as np

LOG = []            # log de qualidade: (tabela, problema, n, decisão)
def log(tabela, problema, n, decisao, exemplo=None):
    LOG.append({"tabela": tabela, "problema": problema, "linhas": int(n), "decisao": decisao, "exemplo": exemplo})

def sem_depois(itens):
    """Log no formato dos Protótipos 3 a 5 (sem a contagem depois), para manter os pacotes reproduzíveis."""
    return [{k: v for k, v in q.items() if k != "depois"} for q in itens]

# --------------------------------------------------------------------------- origem
def carregar(pasta):
    ler = lambda n: pd.read_csv(os.path.join(pasta, n), dtype=str, keep_default_na=True)
    return {
        "equipes": ler("equipes.csv"),
        "resultados": ler("resultados_ciclos.csv"),
        "eixo3": ler("eixo3_indicadores.csv"),
        "nps": ler("nps_atributos.csv"),
        "planos": ler("planos_acao.csv"),
    }

# --------------------------------------------------------------------------- utilidades
ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
CICLOS = [f"{a}.{q}" for a in range(2023, 2027) for q in (1, 2, 3)][:11]   # 2023.1 ... 2026.2

def norm_ciclo(c):
    c = str(c).strip()
    m = re.match(r"^(\d{4})[.\-Q](\d)$", c)
    if m: return f"{m.group(1)}.{m.group(2)}"
    m = re.match(r"^(\d)/(\d{4})$", c)
    if m: return f"{m.group(2)}.{m.group(1)}"
    return None

def norm_distrito(d):
    m = re.search(r"\b(VIII|VII|VI|IV|V|III|II|I)\b", str(d).upper())
    return f"DS {m.group(1)}" if m else None

def norm_tipo(t):
    t = re.sub(r"[^a-z]", "", str(t).lower())
    return {"esf": "eSF", "esb": "eSB", "emulti": "eMulti"}.get(t)

def num(s):
    return pd.to_numeric(s.astype(str).str.strip().str.replace(",", ".", regex=False), errors="coerce")

# parâmetros do programa por modo: limiares e máximos ficam aqui, nunca espalhados pelo código
PARAMETROS = {
    "manual": {      # Manual de Avaliação (v. 02.03.26): zonas no Quadro 10, blocos no Quadro 4
        "zonas": [("Excelência", 900), ("Qualidade", 800), ("Aperfeiçoamento", 600), ("Crítica", 400), ("Insuficiente", 0)],
        "blocos": {"a": 40, "b": 80, "c": 80}},
    "dicionario": {  # DICIONARIO_DE_DADOS.md da base sintética (regra 6 e domínios dos blocos)
        "zonas": [("Excelência", 850), ("Qualidade", 700), ("Aperfeiçoamento", 550), ("Crítica", 400), ("Insuficiente", 0)],
        "blocos": {"a": 80, "b": 60, "c": 60}},
}
BLOCOS_BASE = PARAMETROS["dicionario"]["blocos"]   # máximos com que a base sintética foi gerada
MODO = "manual"
ZONAS, BLOCOS = PARAMETROS[MODO]["zonas"], PARAMETROS[MODO]["blocos"]

def usar_modo(modo):
    global MODO, ZONAS, BLOCOS
    MODO = modo; ZONAS, BLOCOS = PARAMETROS[modo]["zonas"], PARAMETROS[modo]["blocos"]

def zona(p):
    if pd.isna(p): return None
    for n, v in ZONAS:
        if p >= v: return n
    return "Insuficiente"

# --------------------------------------------------------------------------- limpeza
def limpar(t):
    eq, rc, e3, nps, pa = t["equipes"].copy(), t["resultados"].copy(), t["eixo3"].copy(), t["nps"].copy(), t["planos"].copy()

    # ---- equipes
    d0 = eq.distrito_sanitario.copy(); eq["distrito_sanitario"] = eq.distrito_sanitario.map(norm_distrito)
    log("equipes", "distrito_sanitario com 19 grafias (maiúsculas, sem acento, 'ds v')", (~d0.str.match(r"^Distrito Sanitário (I|II|III|IV|V|VI|VII|VIII)$")).sum(),
        "normalizado para 'DS <romano>' por regex", sorted(d0.unique())[:6])
    t0 = eq.tipo_equipe.copy(); eq["tipo_equipe"] = eq.tipo_equipe.map(norm_tipo)
    log("equipes", "tipo_equipe com variações (e-SF, ESF, ' eSF', esb...)", (t0.str.strip() != eq.tipo_equipe).sum(), "normalizado para eSF / eSB / eMulti", sorted(t0.unique()))
    u0 = eq.nome_unidade.copy(); eq["nome_unidade"] = eq.nome_unidade.str.strip()
    log("equipes", "nome_unidade com espaços nas bordas (13 CNES com 2 grafias)", (u0 != eq.nome_unidade).sum(), "strip; CNES passa a ter 1 nome")
    eq["populacao_adscrita"] = num(eq.populacao_adscrita); eq["n_profissionais"] = num(eq.n_profissionais).astype(int); eq["grupo"] = eq.grupo.astype(int)
    log("equipes", "populacao_adscrita ausente", eq.populacao_adscrita.isna().sum(), "mantido nulo; normalização por porte usa n_profissionais")
    log("equipes", "n_profissionais máximo 53 (cliente informou até 80)", 0, "registrado como divergência a confirmar com o cliente")

    # ---- ciclos em todas as tabelas
    for nome, df in (("resultados", rc), ("eixo3", e3), ("nps", nps), ("planos", pa)):
        c0 = df.ciclo.copy(); df["ciclo"] = df.ciclo.map(norm_ciclo)
        if (c0 != df.ciclo).sum(): log(nome, "ciclo em 4 formatos (AAAA.Q, AAAA-Q, AAAAQn, Q/AAAA)", (c0 != df.ciclo).sum(), "normalizado para AAAA.Q")
        assert df.ciclo.notna().all()

    # ---- resultados
    n0 = len(rc); rc = rc.drop_duplicates(["codigo_ine", "ciclo"]).copy()
    log("resultados", "equipe+ciclo duplicados (mesmo conteúdo, ciclo grafado diferente)", n0 - len(rc), "mantida 1 linha por equipe+ciclo")
    orf = ~rc.codigo_ine.isin(eq.codigo_ine); log("resultados", "codigo_ine sem cadastro em equipes.csv (INE 7xxxxxxxxx)", orf.sum(), "excluídos do painel; listados para o cliente", rc[orf].codigo_ine.head(3).tolist())
    rc = rc[~orf].copy()
    zraw = rc.zona_classificacao.copy()
    for c in ["eixo1_bloco_a", "eixo1_bloco_b", "eixo1_bloco_c", "eixo1_total", "taxa_resposta_bloco_a", "eixo2_total", "eixo3_total", "pontuacao_final"]:
        raw = rc[c].copy(); rc[c] = num(rc[c])
        virg = raw.astype(str).str.contains(",", na=False).sum()
        if virg: log("resultados", f"{c} com vírgula decimal", virg, "convertido para ponto")
    rc["desclassificada"] = rc.situacao_participacao.eq("Desclassificada")
    log("resultados", "situacao_participacao = Desclassificada (sem pontuação)", rc.desclassificada.sum(), "mantida como ausência de dado, nunca como zero (regra 2)")
    rc["bloco_a_valido"] = rc.bloco_a_valido.eq("True")
    viol = rc.taxa_resposta_bloco_a.between(0, 0.2999) & rc.bloco_a_valido
    log("resultados", "taxa < 30% mas bloco_a_valido = True (viola regra 1)", viol.sum(), "recalculado: bloco_a_valido = taxa >= 0,30", rc.loc[viol, "taxa_resposta_bloco_a"].tolist())
    rc.loc[viol, "bloco_a_valido"] = False
    bad_taxa = ~rc.taxa_resposta_bloco_a.between(0, 1) & rc.taxa_resposta_bloco_a.notna()
    log("resultados", "taxa_resposta_bloco_a fora de [0,1]", bad_taxa.sum(), "taxa anulada; validade do Bloco A mantida como veio", rc.loc[bad_taxa, "taxa_resposta_bloco_a"].unique().tolist())
    rc.loc[bad_taxa, "taxa_resposta_bloco_a"] = np.nan
    inv = (~rc.bloco_a_valido) & rc.eixo1_bloco_a.notna()
    log("resultados", "Bloco A inválido registrado como 0 e somado ao Eixo 1 (regra 1 diz 'não computado')", inv.sum(),
        "mantido como a plataforma calcula (0 pts) e sinalizado; a IA trata como 'não avaliado', não como desempenho ruim")
    # eixo 2 ausente em 2023 mas incluído na pontuação final
    e2null = rc.eixo2_total.isna() & rc.pontuacao_final.notna()
    rc["eixo2_reconstruido"] = False
    outl = ~rc.pontuacao_final.between(0, 1000) & rc.pontuacao_final.notna()
    rec = e2null & ~outl
    rc.loc[rec, "eixo2_total"] = (rc.pontuacao_final - rc.eixo1_total - rc.eixo3_total).round(1)
    rc.loc[rec, "eixo2_reconstruido"] = True
    log("resultados", "eixo2_total ausente nos 3 ciclos de 2023, embora pontuacao_final o inclua", e2null.sum(), "reconstruído como final - eixo1 - eixo3 (sinalizado)")
    # outliers de pontuação
    log("resultados", "pontuacao_final impossível (-35, 1247, 1580, 9999)", outl.sum(), "recalculada como eixo1 + eixo2 + eixo3; eixo2 ausente estimado pela média do NPS + 100",
        rc.loc[outl, "pontuacao_final"].unique().tolist())
    # eixo2 estimado por NPS quando ainda nulo
    npsn = nps.copy(); npsn["nps"] = num(npsn.nps)
    npsm = npsn.groupby(["codigo_ine", "ciclo"]).nps.mean().rename("nps_medio").reset_index()
    rc = rc.merge(npsm, on=["codigo_ine", "ciclo"], how="left")
    still = rc.eixo2_total.isna() & ~rc.desclassificada
    rc.loc[still, "eixo2_total"] = (rc.loc[still, "nps_medio"] + 100).round(1); rc.loc[still, "eixo2_reconstruido"] = True
    rc.loc[outl, "pontuacao_final"] = (rc.eixo1_total + rc.eixo2_total + rc.eixo3_total).round(1)
    if MODO == "manual":
        # alinhamento da base sintética ao Manual de Avaliação (a base veio com A=80, B=60, C=60 e zonas 850/700/550/400)
        rc["eixo1_bloco_a"] = (rc.eixo1_bloco_a * BLOCOS["a"] / BLOCOS_BASE["a"]).round(1)
        rc["eixo1_bloco_b"] = (rc.eixo1_bloco_b * BLOCOS["b"] / BLOCOS_BASE["b"]).round(1)
        rc["eixo1_bloco_c"] = (rc.eixo1_bloco_c * BLOCOS["c"] / BLOCOS_BASE["c"]).round(1)
        rc["eixo1_total"] = (rc.eixo1_bloco_a.fillna(0) + rc.eixo1_bloco_b + rc.eixo1_bloco_c).round(1)
        rc.loc[rc.desclassificada, "eixo1_total"] = np.nan
        rc["pontuacao_final"] = (rc.eixo1_total + rc.eixo2_total + rc.eixo3_total).round(1)
        log("resultados", "máximos dos blocos do Eixo 1 vieram como A=80, B=60, C=60; Manual define A=40, B=80, C=80", (~rc.desclassificada).sum(), "base sintética reescalada proporcionalmente para os máximos do Manual; pontuação final recomposta")
        # zona recalculada
        rc["zona_classificacao"] = rc.pontuacao_final.map(zona)
        log("resultados", "zonas vieram com faixas 850/700/550/400 (dicionário); Manual define 900/800/600/400", (zraw.notna() & (zraw != rc.zona_classificacao)).sum(), "zona recalculada pelas faixas do Manual (Quadro 10) sobre a pontuação recomposta")
    else:
        # base como veio (v1.0): só a zona é recalculada, pelas faixas do dicionário; divergências registradas
        rc["zona_classificacao"] = rc.pontuacao_final.map(zona)
        log("resultados", "zona_classificacao incoerente com a pontuação original (linhas com outlier)", (zraw.notna() & (zraw != rc.zona_classificacao)).sum(), "recalculada pelas faixas do dicionário (850/700/550/400)")
        log("resultados", "faixas de zona do dicionário (850/700/550/400) divergem do Manual de Avaliação (900/800/600/400)", 0, "adotadas as faixas do dicionário, que são as que os dados seguem; divergência levada ao cliente")
        log("resultados", "máximos dos blocos do Eixo 1 (A=80, B=60, C=60) divergem do Manual (A=40, B=80, C=80)", 0, "adotados os máximos do dicionário; divergência levada ao cliente")
    falt = 11 * len(eq) - len(rc)
    log("resultados", "equipes sem linha em alguns ciclos (adesão voluntária)", falt, "ausência tratada como 'não participou', não como queda")

    # ---- eixo 3
    for c in ["peso_maximo", "percentual_alcancado", "pontos_obtidos"]: e3[c] = num(e3[c])
    pct = e3.percentual_alcancado > 1
    log("eixo3", "percentual_alcancado em escala 0-100 em vez de 0-1", pct.sum(), "dividido por 100; pontos_obtidos conferidos = pct x peso")
    e3.loc[pct, "percentual_alcancado"] = e3.loc[pct, "percentual_alcancado"] / 100
    e3["pontos_obtidos"] = (e3.percentual_alcancado * e3.peso_maximo).round(1)
    e3 = e3[e3.codigo_ine.isin(eq.codigo_ine)].drop_duplicates(["codigo_ine", "ciclo", "codigo_indicador"])
    log("eixo3", "IND03 e IND08 (odontologia) não se aplicam ao grupo 4; pesos variam por grupo", 0, "recomendações só citam indicadores aplicáveis ao grupo da equipe (regra 3)")

    # ---- nps
    nps["nps"] = num(nps.nps); nps["n_respondentes"] = num(nps.n_respondentes)
    log("nps", "nps ausente em atributos isolados", nps.nps.isna().sum(), "mantido nulo; média do ciclo ignora o atributo ausente")
    log("nps", "5 atributos (acolhimento, espera, resolutividade, estrutura, vínculo) e conversão eixo2 = média NPS + 100, diferentes do Manual (6 perguntas, Quadro 7 por faixas)", 0, "mantido o esquema dos dados como simplificação da base sintética; conversão oficial (Quadro 7) entra com os dados reais" if MODO == "manual" else "adotado o esquema dos dados; divergência levada ao cliente")
    nps = nps[nps.codigo_ine.isin(eq.codigo_ine)].drop_duplicates(["codigo_ine", "ciclo", "codigo_atributo"])

    # ---- planos
    vazio = pa.texto_plano.fillna("").str.strip().eq("")
    log("planos", "texto_plano vazio ou nulo", vazio.sum(), "mantido com marcador 'sem texto'; excluído da análise de linguagem")
    pa.loc[vazio, "texto_plano"] = None
    for c in ["dim_governanca", "dim_smart", "dim_viabilidade", "nivel_maturidade"]: pa[c] = num(pa[c]).astype(int)
    log("planos", "textos repetidos (modelos padrão)", pa.texto_plano.dropna().duplicated().sum(), "mantidos; indício de planos genéricos, insumo para a IA")

    return eq, rc, e3, nps, pa

# --------------------------------------------------------------------------- contagem depois do tratamento
def anotar_depois(eq, rc, e3, nps, pa):
    """Reaplica cada verificação do LOG sobre as tabelas tratadas e grava em "depois" quantas linhas
    ainda têm o problema. 0 = corrigido; igual a "linhas" = mantido e sinalizado (decisão registrada)."""
    canon = rc.pontuacao_final.map(zona)
    regras = [
        ("distrito_sanitario", lambda: (~eq.distrito_sanitario.isin([f"DS {r}" for r in ROMANOS])).sum()),
        ("tipo_equipe", lambda: (~eq.tipo_equipe.isin(["eSF", "eSB", "eMulti"])).sum()),
        ("nome_unidade", lambda: (eq.nome_unidade != eq.nome_unidade.str.strip()).sum()),
        ("populacao_adscrita", lambda: eq.populacao_adscrita.isna().sum()),
        ("n_profissionais", lambda: 0),
        ("ciclo em 4 formatos", lambda: (~rc.ciclo.str.match(r"^\d{4}\.\d$")).sum()),
        ("equipe+ciclo duplicados", lambda: rc.duplicated(["codigo_ine", "ciclo"]).sum()),
        ("codigo_ine sem cadastro", lambda: (~rc.codigo_ine.isin(eq.codigo_ine)).sum()),
        ("eixo2_total com vírgula", lambda: 0),        # coluna convertida para número
        ("situacao_participacao", lambda: rc.desclassificada.sum()),
        ("taxa < 30%", lambda: ((rc.taxa_resposta_bloco_a < 0.3) & rc.bloco_a_valido).sum()),
        ("taxa_resposta_bloco_a fora", lambda: (~rc.taxa_resposta_bloco_a.between(0, 1) & rc.taxa_resposta_bloco_a.notna()).sum()),
        ("Bloco A inválido", lambda: ((~rc.bloco_a_valido) & rc.eixo1_bloco_a.notna()).sum()),
        ("eixo2_total ausente", lambda: (rc.eixo2_total.isna() & ~rc.desclassificada).sum()),
        ("pontuacao_final impossível", lambda: (~rc.pontuacao_final.between(0, 1000) & rc.pontuacao_final.notna()).sum()),
        ("máximos dos blocos do Eixo 1 vieram", lambda: ((rc.eixo1_bloco_a > BLOCOS["a"]) | (rc.eixo1_bloco_b > BLOCOS["b"]) | (rc.eixo1_bloco_c > BLOCOS["c"])).sum()),
        ("zonas vieram", lambda: (rc.pontuacao_final.notna() & (rc.zona_classificacao != canon)).sum()),
        ("zona_classificacao incoerente", lambda: (rc.pontuacao_final.notna() & (rc.zona_classificacao != canon)).sum()),
        ("faixas de zona", lambda: 0), ("máximos dos blocos do Eixo 1 (", lambda: 0),
        ("equipes sem linha", lambda: 11 * len(eq) - len(rc)),
        ("percentual_alcancado", lambda: (e3.percentual_alcancado > 1).sum()),
        ("IND03", lambda: 0),
        ("nps ausente", lambda: nps.nps.isna().sum()),
        ("5 atributos", lambda: 0),
        ("texto_plano vazio", lambda: pa.texto_plano.isna().sum()),
        ("textos repetidos", lambda: pa.texto_plano.dropna().duplicated().sum()),
    ]
    for q in LOG:
        if "depois" in q: continue
        f = next((f for k, f in regras if q["problema"].startswith(k)), None)
        assert f is not None, q["problema"]
        q["depois"] = int(f())

def perfilar(t, eq, rc, e3, nps, pa):
    """Perfilamento resumido para a tela de análise do Protótipo 6: volume antes/depois, chaves e completude da base crua."""
    limpas = {"equipes": eq, "resultados": rc, "eixo3": e3, "nps": nps, "planos": pa}
    chave = {"equipes": ["codigo_ine"], "resultados": ["codigo_ine", "ciclo"], "eixo3": ["codigo_ine", "ciclo", "codigo_indicador"],
             "nps": ["codigo_ine", "ciclo", "codigo_atributo"], "planos": ["id_plano"]}
    out = []
    for n, df in t.items():
        out.append({"tabela": n, "cruas": len(df), "limpas": len(limpas[n]), "colunas": df.shape[1], "chave": "+".join(chave[n]),
                    "chave_unica_crua": bool(not df.duplicated(chave[n]).any()), "chave_unica_limpa": bool(not limpas[n].duplicated(chave[n]).any()),
                    "completude": {c: round(float(df[c].notna().mean()), 4) for c in df.columns}})
    return out

# --------------------------------------------------------------------------- pacote para o protótipo
IND_NOMES = {
    "IND01": "Gestantes com 6+ consultas de pré-natal", "IND02": "Gestantes com exames de sífilis e HIV", "IND03": "Gestantes com atendimento odontológico",
    "IND04": "Citopatológico do colo do útero", "IND05": "Vacinação polio e penta em menores de 1 ano", "IND06": "Hipertensos com PA aferida",
    "IND07": "Diabéticos com hemoglobina glicada", "IND08": "Primeira consulta odontológica programática", "IND09": "Demanda espontânea resolvida na APS", "IND10": "Visitas domiciliares por ACS"}
ATR_NOMES = {"ATR1": "Acolhimento da equipe", "ATR2": "Tempo de espera", "ATR3": "Resolutividade", "ATR4": "Estrutura e limpeza", "ATR5": "Vínculo e confiança"}

BAIRROS = {
    "DS I": ["Boa Vista", "Santo Amaro", "Coelhos", "Ilha Joana Bezerra", "São José", "Cabanga", "Paissandu", "Soledade", "Coque"],
    "DS II": ["Água Fria", "Campina do Barreto", "Arruda", "Beberibe", "Cajueiro", "Fundão", "Linha do Tiro", "Encruzilhada", "Ponto de Parada"],
    "DS III": ["Casa Amarela", "Nova Descoberta", "Macaxeira", "Vasco da Gama", "Alto do Mandu", "Córrego do Jenipapo", "Apipucos", "Poço da Panela", "Alto José do Pinho"],
    "DS IV": ["Várzea", "Iputinga", "Cordeiro", "Engenho do Meio", "Torrões", "Caxangá", "Cidade Universitária", "Zumbi", "Roda de Fogo"],
    "DS V": ["Afogados", "Mangueira", "Mustardinha", "Jardim São Paulo", "Estância", "Bongi", "San Martin", "Curado", "Jiquiá", "Totó", "Coqueiral", "Sancho", "Areias"],
    "DS VI": ["Ibura", "Jordão", "Imbiribeira", "Pina", "Brasília Teimosa", "Boa Viagem", "Ipsep", "Cohab", "Areias"],
    "DS VII": ["Guabiraba", "Pau Ferro", "Passarinho", "Brejo da Guabiraba", "Sítio dos Pintos", "Dois Irmãos", "Nova Guabiraba", "Córrego da Fortuna", "Brejo de Beberibe"],
    "DS VIII": ["Ibura de Baixo", "Lagoa Encantada", "UR-10", "Três Carneiros", "Monte Verde", "Vila do Sesi", "Jardim Monte Verde", "UR-5", "Cohab Ibura"]}
ROM = ["I", "II", "III", "IV", "V", "VI"]

def nomear(eq):
    """Nomes fictícios de unidades e equipes, por bairro do distrito (base sintética). CNES e INE permanecem como chave."""
    eq = eq.copy(); unidade = {}; usados = {}
    for ds, g in eq.sort_values(["distrito_sanitario", "codigo_cnes"]).groupby("distrito_sanitario", sort=False):
        nomes = BAIRROS.get(ds, [ds]); i = 0
        for cnes in g.codigo_cnes.unique():
            base = nomes[i % len(nomes)]; n = usados.get((ds, base), 0); usados[(ds, base)] = n + 1
            unidade[cnes] = f"USF {base}" + (f" {ROM[n]}" if n else ""); i += 1
    eq["nome_unidade_original"] = eq.nome_unidade; eq["nome_unidade"] = eq.codigo_cnes.map(unidade)
    eq["nome_equipe_original"] = eq.nome_equipe
    cont = {}
    rot = []
    for _, q in eq.iterrows():
        k = (q.codigo_cnes, q.tipo_equipe); cont[k] = cont.get(k, 0) + 1; rot.append(cont[k])
    eq["_seq"] = rot
    tot = eq.groupby(["codigo_cnes", "tipo_equipe"])._seq.transform("max")
    bairro = eq.nome_unidade.str.replace("USF ", "", regex=False)
    eq["nome_equipe"] = [f"{t} {b}" + (f" {ROM[s - 1]}" if m > 1 else "") for t, b, s, m in zip(eq.tipo_equipe, bairro, eq._seq, tot)]
    return eq.drop(columns="_seq")

def empacotar(eq, rc, e3, nps, pa):
    if MODO == "manual":
        eq = nomear(eq)
        log("equipes", "nomes de unidades (USF V-842) e equipes (Equipe 001) são códigos sintéticos", len(eq), "substituídos por nomes fictícios de bairros do distrito; CNES e INE preservados como chave")
        LOG[-1]["depois"] = int(eq.nome_unidade.str.match(r"^USF [IVX]+-\d+$").sum())
    else:   # v1.0: rótulo sintético original, "eSF 001 · USF V-842"
        eq = eq.copy(); eq["nome_equipe_original"] = eq.nome_equipe
        eq["nome_equipe"] = eq.tipo_equipe + " " + eq.nome_equipe.str.replace("Equipe ", "", regex=False) + " · " + eq.nome_unidade
    r = lambda x: None if pd.isna(x) else round(float(x), 1)
    teams = []
    e3g = {k: g for k, g in e3.groupby(["codigo_ine", "ciclo"])}
    npg = {k: g for k, g in nps.groupby(["codigo_ine", "ciclo"])}
    pag = {k: g for k, g in pa.groupby("codigo_ine")}
    for _, q in eq.sort_values("codigo_ine").iterrows():
        ine = q.codigo_ine
        res = {}
        for _, x in rc[rc.codigo_ine == ine].iterrows():
            if x.desclassificada:
                res[x.ciclo] = {"d": 1}; continue
            k = (ine, x.ciclo)
            ind = {}
            if k in e3g:
                for _, i in e3g[k].iterrows(): ind[i.codigo_indicador] = [round(float(i.percentual_alcancado), 3), int(i.peso_maximo)]
            at = {}
            if k in npg:
                for _, i in npg[k].iterrows(): at[i.codigo_atributo] = [r(i.nps), int(i.n_respondentes)]
            res[x.ciclo] = {"a": r(x.eixo1_bloco_a), "b": r(x.eixo1_bloco_b), "c": r(x.eixo1_bloco_c), "e1": r(x.eixo1_total), "e2": r(x.eixo2_total), "e3": r(x.eixo3_total),
                            "f": r(x.pontuacao_final), "z": x.zona_classificacao, "tx": r(x.taxa_resposta_bloco_a), "av": bool(x.bloco_a_valido), "e2r": bool(x.eixo2_reconstruido), "ind": ind, "atr": at}
        planos = [{"id": p.id_plano, "c": p.ciclo, "t": None if pd.isna(p.texto_plano) else p.texto_plano, "g": int(p.dim_governanca), "s": int(p.dim_smart), "v": int(p.dim_viabilidade), "n": int(p.nivel_maturidade), "r": p.rotulo_maturidade}
                  for _, p in pag.get(ine, pd.DataFrame()).iterrows()]
        equipe = {"ine": ine, "cnes": q.codigo_cnes, "usf": q.nome_unidade, "nome": q.nome_equipe, "eq": q.nome_equipe_original}
        if MODO == "manual": equipe["cod"] = q.nome_equipe_original.replace("Equipe ", "")
        teams.append({**equipe, "ds": q.distrito_sanitario, "tipo": q.tipo_equipe, "grupo": int(q.grupo), "pop": None if pd.isna(q.populacao_adscrita) else int(q.populacao_adscrita),
                      "prof": int(q.n_profissionais), "res": res, "planos": planos})
    return {"meta": {"sintetico": True, "ciclos": CICLOS, "gerado_em": "2026-09-24", "fonte": "datos_sinteticos_recife_monitora_projetos_5 (cliente, 24/09/2026)",
                     "zonas": [list(z) for z in ZONAS], "blocos": BLOCOS, "ind": IND_NOMES, "atr": ATR_NOMES},
            "qualidade": LOG, "equipes": teams}

def gerar(entrada, modo):
    """Roda limpeza e empacotamento em um modo; devolve tabelas tratadas, pacote e perfil."""
    LOG.clear(); usar_modo(modo)
    t = carregar(entrada)
    eq, rc, e3, nps, pa = limpar(t)
    pac = empacotar(eq, rc, e3, nps, pa)
    anotar_depois(eq, rc, e3, nps, pa)
    return (eq, rc, e3, nps, pa), pac, perfilar(t, eq, rc, e3, nps, pa)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--entrada", required=True); ap.add_argument("--saida", required=True)
    ap.add_argument("--modo", choices=list(PARAMETROS), default="manual", help="parâmetros do programa: manual (v1.1, Protótipo 5) ou dicionario (v1.0, Protótipos 3 e 4)")
    ap.add_argument("--pacote", choices=["v5", "v6"], default="v5", help="v6 gera rastreia_data_v6.json com os dois modos (Protótipo 6)")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.saida, "limpo"), exist_ok=True)
    if a.pacote == "v6":
        modos = {}
        for m in ("manual", "dicionario"):
            _, pac, perfil = gerar(a.entrada, m)
            modos[m] = {"meta": pac["meta"], "qualidade": [dict(q) for q in LOG], "equipes": pac["equipes"]}
        v6 = {"meta": {"versao": "v6", "sintetico": True, "modo_padrao": "manual", "gerado_em": pac["meta"]["gerado_em"], "fonte": pac["meta"]["fonte"],
                       "comando": "python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida --pacote v6", "perfil": perfil},
              "modos": modos}
        json.dump(v6, open(os.path.join(a.saida, "rastreia_data_v6.json"), "w"), ensure_ascii=False, separators=(",", ":"))
        print(f"pacote v6: modos={list(modos)} problemas_logados={[len(x['qualidade']) for x in modos.values()]} equipes={len(modos['manual']['equipes'])}")
        return
    (eq, rc, e3, nps, pa), pac, _ = gerar(a.entrada, a.modo)
    for n, df in (("equipes", eq), ("resultados_ciclos", rc), ("eixo3_indicadores", e3), ("nps_atributos", nps), ("planos_acao", pa)):
        df.to_csv(os.path.join(a.saida, "limpo", f"{n}.csv"), index=False)
    json.dump(LOG, open(os.path.join(a.saida, "qualidade_dados.json"), "w"), ensure_ascii=False, indent=1)
    pac["qualidade"] = sem_depois(LOG)
    json.dump(pac, open(os.path.join(a.saida, "rastreia_data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"modo={MODO} equipes={len(eq)} resultados={len(rc)} eixo3={len(e3)} nps={len(nps)} planos={len(pa)} problemas_logados={len(LOG)}")

if __name__ == "__main__":
    main()
