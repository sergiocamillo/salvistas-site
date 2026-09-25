"""Converte o dump da REST API do WordPress (raw/*.json) em Markdown + inventários."""
import glob, json, os, re, html
from collections import Counter
from markdownify import markdownify as md

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")


def load(kind):
    out = []
    for f in sorted(glob.glob(f"{RAW}/api-{kind}-*.json"), key=lambda p: int(re.findall(r"-(\d+)\.json", p)[0])):
        out += json.load(open(f))
    return out


def clean(h):
    h = re.sub(r"\[/?(vc_|et_|av_|fusion_|su_)[^\]]*\]", "", h or "")  # shortcodes de page builder
    text = md(h, heading_style="ATX", strip=["script", "style"])
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def title(o):
    return html.unescape(o["title"]["rendered"]).strip()


cats = {c["id"]: c["name"] for c in load("categories")}
tags = load("tags")
tagname = {t["id"]: t["name"] for t in tags}
media = load("media")
pages = load("pages")
posts = load("posts")
portfolio = load("portfolio")

# ---------- páginas ----------
os.makedirs(f"{ROOT}/paginas", exist_ok=True)
byid = {p["id"]: p for p in pages}


def path_of(p):
    parts = [p["slug"]]
    while p["parent"] and p["parent"] in byid:
        p = byid[p["parent"]]
        parts.insert(0, p["slug"])
    return "/".join(parts)


idx = ["# Páginas (WordPress)\n", "| Caminho | Título | Palavras | Modificada |", "|---|---|---|---|"]
for p in sorted(pages, key=path_of):
    body = clean(p["content"]["rendered"])
    words = len(body.split())
    fn = path_of(p).replace("/", "__") + ".md"
    with open(f"{ROOT}/paginas/{fn}", "w") as fh:
        fh.write(f"---\ntitulo: {title(p)}\nurl: {p['link']}\nmodificada: {p['modified']}\npalavras: {words}\n---\n\n# {title(p)}\n\n{body}\n")
    idx.append(f"| `/{path_of(p)}` | {title(p)} | {words} | {p['modified'][:10]} |")
open(f"{ROOT}/paginas/_INDEX.md", "w").write("\n".join(idx) + "\n")

# ---------- posts ----------
os.makedirs(f"{ROOT}/posts", exist_ok=True)
rows, years, catcount = [], Counter(), Counter()
for p in posts:
    body = clean(p["content"]["rendered"])
    words = len(body.split())
    y = p["date"][:4]
    years[y] += 1
    cs = [cats.get(c, str(c)) for c in p["categories"]]
    for c in cs:
        catcount[c] += 1
    ts = [tagname.get(t, str(t)) for t in p["tags"]]
    os.makedirs(f"{ROOT}/posts/{y}", exist_ok=True)
    fn = f"{p['date'][:10]}-{p['slug'][:80]}.md"
    with open(f"{ROOT}/posts/{y}/{fn}", "w") as fh:
        fh.write(
            f"---\ntitulo: \"{title(p)}\"\nurl: {p['link']}\ndata: {p['date']}\ncategorias: {cs}\n"
            f"tags: {len(ts)}\nimagem_destacada: {p.get('featured_media')}\npalavras: {words}\n---\n\n# {title(p)}\n\n{body}\n"
        )
    rows.append((p["date"][:10], title(p), ", ".join(cs), words, len(ts), p["link"]))

rows.sort(reverse=True)
with open(f"{ROOT}/posts/_INDEX.md", "w") as fh:
    fh.write(f"# Posts ({len(posts)})\n\n## Por ano\n\n")
    for y in sorted(years):
        fh.write(f"- {y}: {years[y]}\n")
    fh.write("\n## Por categoria\n\n")
    for c, n in catcount.most_common():
        fh.write(f"- {c}: {n}\n")
    fh.write("\n## Lista\n\n| Data | Título | Categorias | Palavras | Tags |\n|---|---|---|---|---|\n")
    for d, t, c, w, nt, l in rows:
        fh.write(f"| {d} | [{t}]({l}) | {c} | {w} | {nt} |\n")

# ---------- portfolio ----------
with open(f"{ROOT}/paginas/_portfolio.md", "w") as fh:
    for p in portfolio:
        fh.write(f"## {title(p)}\n{p['link']}\n\n{clean(p['content']['rendered'])}\n\n")

# ---------- mídia ----------
with open(f"{ROOT}/imagens/_INDEX.md", "w") as fh:
    fh.write("| ID | Título | Tamanho | URL |\n|---|---|---|---|\n")
    for m in media:
        d = m.get("media_details", {}) or {}
        fh.write(f"| {m['id']} | {title(m)} | {d.get('width')}x{d.get('height')} | {m['source_url']} |\n")

# ---------- tags ----------
tc = Counter({t["name"]: t["count"] for t in tags})
with open(f"{ROOT}/_tags-resumo.md", "w") as fh:
    fh.write(f"# Tags: {len(tags)} no total\n\n")
    fh.write(f"- Tags usadas 1 vez ou menos: {sum(1 for t in tags if t['count'] <= 1)}\n\n## Top 60\n\n")
    for n, c in tc.most_common(60):
        fh.write(f"- {n}: {c}\n")

print(len(pages), "páginas;", len(posts), "posts;", len(media), "mídias;", len(tags), "tags")
print("anos:", dict(sorted(years.items())))
print("categorias:", catcount.most_common())
