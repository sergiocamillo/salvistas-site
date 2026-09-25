"""Triagem dos posts: separa conteúdo próprio da Fraternidade de notícias replicadas.

Gera triagem.csv (todos os posts com nota e decisão) e ../docs/02-triagem-blog.md.
"""
import csv, glob, html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")

posts = []
for f in glob.glob(f"{RAW}/api-posts-*.json"):
    posts += json.load(open(f))
cats = {}
for f in glob.glob(f"{RAW}/api-categories-*.json"):
    cats.update({c["id"]: c["name"] for c in json.load(open(f))})

# Sinais de conteúdo próprio (peso) e de conteúdo replicado (peso negativo)
PROPRIO = {
    r"salvista": 4, r"\bsjs\b": 4, r"fraternidade jesus salvador": 5, r"servos de jesus salvador": 5,
    r"servas de jesus salvador": 5, r"gilberto": 4, r"pentecostes": 3, r"bororé|borore": 5,
    r"seminário nossa senhora": 4, r"ordena[çc][ãa]o": 2, r"\bvotos\b": 2, r"profiss[ãa]o": 1,
    r"noviciado|postulante|aspirante": 3, r"juventude salvista": 5, r"s\.e\.r\.|servos evangelizadores": 3,
    r"grajaú|grajau|parelheiros": 3, r"douradina|dourados": 3, r"fréjus|frejus|six-fours": 4,
    r"lamezia|gizzeria": 4, r"coimbra|tentúgal|tentugal|arazede|meãs": 4, r"belém do pará": 2,
    r"testemunho": 1, r"minha vocação": 3, r"prior geral": 4, r"cap[íi]tulo geral": 4,
    r"acamp": 2, r"providência santíssima": 3, r"padrinho|madrinha": 2,
}
REPLICADO = {
    r"\bfonte\b": -3, r"cnbb": -2, r"news\.va|rádio vaticano|radio vaticano": -3, r"zenit|acidigital|gaudium": -3,
    r"agenciacatolica|agência católica": -3, r"^evangelho ": -6, r"leituras relacionadas": -6,
    r"intenç[õo]es do (santo padre|papa)": -4, r"audiência": -2, r"homilia do papa": -3,
    r"^(papa|bento xvi|card|dom |cnbb|bispo)": -4, r"best games": -100, r"apkticket": -100,
}

rows = []
for p in posts:
    t = html.unescape(p["title"]["rendered"]).strip()
    body = re.sub(r"<[^>]+>", " ", p["content"]["rendered"])
    text = f"{t}\n{body}".lower()
    score = 0
    hits = []
    for rx, w in {**PROPRIO, **REPLICADO}.items():
        target = t.lower() if rx.startswith("^") else text
        n = len(re.findall(rx, target, flags=re.M))
        if n:
            score += w * min(n, 3)
            hits.append(rx.strip("\\b^"))
    cs = [cats.get(c, "") for c in p["categories"]]
    if "Salvistas em Missão" in cs:
        score += 6
    if "Salvistas" in cs:
        score += 2
    words = len(body.split())
    if words < 60:
        score -= 3
    if score <= -50:
        dec = "apagar (spam)"
    elif score >= 10:
        dec = "migrar"
    elif score >= 4:
        dec = "revisar"
    else:
        dec = "redirecionar"
    rows.append({"decisao": dec, "nota": score, "data": p["date"][:10], "titulo": t, "categorias": ", ".join(cs),
                 "palavras": words, "sinais": " ".join(hits[:8]), "slug": p["slug"], "id": p["id"], "url": p["link"]})

rows.sort(key=lambda r: (-r["nota"], r["data"]))
with open(f"{ROOT}/triagem.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

from collections import Counter
cnt = Counter(r["decisao"] for r in rows)
with open(f"{ROOT}/../docs/02-triagem-blog.md", "w") as fh:
    fh.write("# Triagem do blog\n\n")
    fh.write("Classificação automática por sinais de conteúdo próprio (salvista, sjs, missões, Bororé, ordenações...) "
             "contra sinais de notícia replicada (Fonte, CNBB, Vaticano, Evangelho do dia...). "
             "Lista completa com notas: `conteudo-original/triagem.csv`.\n\n")
    for k in ["migrar", "revisar", "redirecionar", "apagar (spam)"]:
        fh.write(f"- **{k}**: {cnt.get(k, 0)}\n")
    fh.write("\nQuem decide o **revisar** é a Fraternidade: cada item vira migrar ou redirecionar.\n")
    for k in ["migrar", "revisar", "apagar (spam)"]:
        fh.write(f"\n## {k.capitalize()}\n\n| Data | Título | Categoria | Palavras |\n|---|---|---|---|\n")
        for r in sorted([r for r in rows if r["decisao"] == k], key=lambda r: r["data"], reverse=True):
            fh.write(f"| {r['data']} | [{r['titulo']}]({r['url']}) | {r['categorias']} | {r['palavras']} |\n")
print(cnt)
