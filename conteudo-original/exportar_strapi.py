"""Gera ../cms/data/importacao.json a partir do dump do WordPress (raw/) e da triagem.

Conteúdo em formato "blocks" do Strapi 5. Imagens ficam como marcadores
{"type": "image", "src": url} que o script de importação do Strapi troca pelo
arquivo enviado para a biblioteca de mídia.
"""
import csv, glob, html, json, os, re, unicodedata
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "..", "cms", "data", "importacao.json")
SITE = "https://salvistas.com.br"


def load(kind):
    out = []
    for f in glob.glob(f"{RAW}/api-{kind}-*.json"):
        out += json.load(open(f))
    return out


# ---------------------------------------------------------------- HTML -> blocks
BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "blockquote", "figure", "table", "section", "article", "center"}


def abs_url(u):
    if not u:
        return u
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("/"):
        return SITE + u
    return u


def full_size(u):
    # WordPress: foto-300x200.jpg -> foto.jpg
    return re.sub(r"-\d{2,4}x\d{2,4}(\.\w+)$", r"\1", u)


def text_node(t, marks):
    n = {"type": "text", "text": t}
    for m in marks:
        n[m] = True
    return n


def inline(node, marks=()):
    """Retorna lista de nós inline + imagens encontradas (como blocos soltos)."""
    out, imgs = [], []
    if isinstance(node, NavigableString):
        t = re.sub(r"[ \t\r\n]+", " ", str(node))
        if t:
            out.append(text_node(t, marks))
        return out, imgs
    if not isinstance(node, Tag):
        return out, imgs
    name = node.name
    if name in ("script", "style", "noscript", "iframe"):
        if name == "iframe" and "youtube" in (node.get("src") or ""):
            imgs.append({"type": "video", "src": node["src"]})
        return out, imgs
    if name == "br":
        out.append(text_node("\n", marks))
        return out, imgs
    if name == "img":
        src = node.get("src") or node.get("data-src")
        if src:
            imgs.append({"type": "image", "src": full_size(abs_url(src)), "alt": node.get("alt", "")})
        return out, imgs
    m = set(marks)
    if name in ("strong", "b"):
        m.add("bold")
    if name in ("em", "i"):
        m.add("italic")
    if name == "u":
        m.add("underline")
    kids, kimgs = [], []
    for c in node.children:
        o, i = inline(c, tuple(sorted(m)))
        kids += o
        kimgs += i
    imgs += kimgs
    if name == "a" and node.get("href") and kids:
        href = abs_url(node["href"])
        # link que só envolve uma imagem: fica a imagem
        if re.search(r"\.(jpe?g|png|gif|webp)$", href, re.I) and not any(k["text"].strip() for k in kids):
            return out, imgs
        out.append({"type": "link", "url": href, "children": kids})
        return out, imgs
    out += kids
    return out, imgs


def tidy(children):
    """Junta textos vizinhos com mesmas marcas, apara bordas; garante filho não vazio."""
    merged = []
    for c in children:
        if merged and c["type"] == "text" and merged[-1]["type"] == "text" and \
                {k: v for k, v in c.items() if k != "text"} == {k: v for k, v in merged[-1].items() if k != "text"}:
            merged[-1]["text"] += c["text"]
        else:
            merged.append(c)
    # apara espaços/quebras no começo e fim
    while merged and merged[0]["type"] == "text" and not merged[0]["text"].strip():
        merged.pop(0)
    while merged and merged[-1]["type"] == "text" and not merged[-1]["text"].strip():
        merged.pop()
    if merged and merged[0]["type"] == "text":
        merged[0]["text"] = merged[0]["text"].lstrip()
    if merged and merged[-1]["type"] == "text":
        merged[-1]["text"] = merged[-1]["text"].rstrip()
    for c in merged:
        if c["type"] == "text":
            c["text"] = re.sub(r" *\n *", "\n", c["text"])
    return merged


def has_text(children):
    for c in children:
        if c["type"] == "text" and c["text"].strip():
            return True
        if c["type"] == "link":
            return True
    return False


def to_blocks(h):
    h = re.sub(r"\[/?(vc_|et_|av_|fusion_|su_|caption)[^\]]*\]", "", h or "")
    soup = BeautifulSoup(h, "html.parser")
    blocks = []
    pending = []  # inline solto fora de <p>

    def flush():
        nonlocal pending
        ch = tidy(pending)
        if has_text(ch):
            blocks.append({"type": "paragraph", "children": ch})
        pending = []

    def emit_para(kind_node, children, imgs, **extra):
        blocks.extend(imgs)
        ch = tidy(children)
        if has_text(ch):
            blocks.append({**extra, "children": ch} if extra else {"type": "paragraph", "children": ch})

    def walk(node):
        for c in list(node.children):
            if isinstance(c, Tag) and c.name in BLOCK_TAGS:
                flush()
                n = c.name
                if n in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    ch, im = inline(c)
                    level = max(2, min(int(n[1]), 4))
                    emit_para(c, ch, im, type="heading", level=level)
                elif n in ("ul", "ol"):
                    items = []
                    for li in c.find_all("li", recursive=False):
                        ch, im = inline(li)
                        blocks.extend(im)
                        ch = tidy(ch)
                        if has_text(ch):
                            items.append({"type": "list-item", "children": ch})
                    if items:
                        blocks.append({"type": "list", "format": "ordered" if n == "ol" else "unordered", "children": items})
                elif n == "blockquote":
                    ch, im = inline(c)
                    emit_para(c, ch, im, type="quote")
                elif n == "p":
                    ch, im = inline(c)
                    emit_para(c, ch, im)
                elif n == "table":
                    for tr in c.find_all("tr"):
                        ch, im = inline(tr)
                        emit_para(tr, ch, im)
                else:  # div, figure, section...
                    walk(c)
            else:
                o, i = inline(c)
                if i:
                    flush()
                    blocks.extend(i)
                pending.extend(o)
        flush()

    walk(soup)
    # paragrafos com "\n\n" viram parágrafos separados? mantemos, o front trata \n como <br>
    return blocks


def plain(h, limit=None):
    t = BeautifulSoup(h or "", "html.parser").get_text(" ")
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    if limit and len(t) > limit:
        t = t[: limit - 1].rsplit(" ", 1)[0] + "…"
    return t


# ---------------------------------------------------------------- posts
media = {m["id"]: m["source_url"] for m in load("media")}
triagem = {int(r["id"]): r for r in csv.DictReader(open(f"{ROOT}/triagem.csv"))}

CATEGORIAS = [
    ("Missões", "missoes", "Notícias das nossas paróquias, casas e obras no Brasil e no mundo.",
     r"miss[ãa]o|mission[áa]ri|bel[ée]m|baixada|fr[ée]jus|fran[çc]a|coimbra|lamezia|hallel|carnaval|bororé"),
    ("Vocação", "vocacao", "Histórias de chamado, formação e consagração.",
     r"voca[çc]|noviciado|seminári|votos|ordena|consagra"),
    ("Juventude", "juventude", "A Juventude Salvista em movimento.", r"juventude|jovens|acamp|enf\b|bote f[ée]"),
    ("Espiritualidade", "espiritualidade", "Louvor, oração, Maria e os santos.",
     r"pentecostes|maria|santa|santo|beato|louvor|ora[çc][ãa]o|m[ãa]e"),
    ("Vida salvista", "vida-salvista", "O dia a dia e a história da Fraternidade Jesus Salvador.", r".*"),
]


def categorize(title, text):
    s = f"{title} {text[:1500]}".lower()
    for nome, slug, _, rx in CATEGORIAS:
        if re.search(rx, s):
            return slug
    return "vida-salvista"


posts_out = []
for p in load("posts"):
    t = triagem.get(p["id"])
    if not t or t["decisao"] not in ("migrar", "revisar"):
        continue
    title = html.unescape(p["title"]["rendered"]).strip()
    if title.isupper():
        title = title.capitalize()
    blocks = to_blocks(p["content"]["rendered"])
    cover = media.get(p.get("featured_media"))
    if not cover:
        first = next((b for b in blocks if b["type"] == "image"), None)
        cover = first["src"] if first else None
    body_text = plain(p["content"]["rendered"])
    posts_out.append({
        "titulo": title,
        "slug": p["slug"],
        "data": p["date"][:10],
        "resumo": plain(p["excerpt"]["rendered"], 280) or body_text[:280],
        "conteudo": blocks,
        "capa": cover,
        "categoria": categorize(title, body_text),
        "publicar": t["decisao"] == "migrar",
        "urlAntiga": p["link"].replace(SITE, ""),
    })

# ---------------------------------------------------------------- orações
pages = {p["slug"]: p for p in load("pages")}


def split_prayers(blocks):
    """Página de São José: cada parágrafo que começa com título em negrito vira uma oração."""
    prayers, cur = [], None
    for b in blocks:
        if b["type"] == "image":
            continue
        first = b.get("children", [{}])[0]
        head = first.get("text", "").strip() if first.get("bold") else ""
        if head and re.match(r"(Ora[çc][ãa]o|Ave|Bendito|Invoca|Preces)", head) and len(head) < 70:
            cur = {"titulo": head.rstrip(":"), "texto": []}
            prayers.append(cur)
            rest = tidy([dict(c) for c in b["children"][1:]])
            if has_text(rest):
                cur["texto"].append({"type": "paragraph", "children": rest})
        elif cur is not None:
            cur["texto"].append(b)
    return prayers


def strip_imgs(blocks):
    return [b for b in blocks if b["type"] not in ("image", "video")]


oracoes = [
    {"titulo": "Oração à Providência Santíssima", "slug": "oracao-a-providencia-santissima",
     "intencao": "Pela Obra da Fraternidade Jesus Salvador, pelos padrinhos e madrinhas",
     "introducao": "Queremos viver da Providência de Deus, no seguimento de Cristo, numa vida pobre segundo o seu exemplo. (Constituições, 13)",
     "texto": [{"type": "paragraph", "children": [{"type": "text", "text":
        "Providência Santíssima do Eterno, Onipotente e Misericordiosíssimo Deus, que tudo tendes providenciado e providenciareis para o nosso bem; providenciai em todas as nossas necessidades. Assim creio, assim espero. Seja sempre feita a vossa santíssima vontade. Amém."}]}],
     "ordem": 2},
    {"titulo": "Oração a Nossa Senhora de Pentecostes", "slug": "oracao-a-nossa-senhora-de-pentecostes",
     "intencao": "Consagração à padroeira da Fraternidade",
     "texto": strip_imgs(to_blocks(pages["oracao-a-nossa-senhora-de-pentecostes"]["content"]["rendered"])),
     "ordem": 1},
]
for i, pr in enumerate(split_prayers(to_blocks(pages["oracoes-a-sao-jose"]["content"]["rendered"]))):
    if not pr["texto"]:
        continue
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", pr["titulo"].lower()).encode("ascii", "ignore").decode()).strip("-")
    if pr["titulo"] == "Oração":
        pr["titulo"], slug = "Oração final a São José", "oracao-final-a-sao-jose"
    oracoes.append({"titulo": pr["titulo"], "slug": slug, "intencao": "Orações a São José, patrono da Fraternidade",
                    "texto": pr["texto"], "ordem": 10 + i})

# ---------------------------------------------------------------- santos
santos = [
    ("O Espírito Santo", "patrono", "Pentecostes",
     "Padroeiro principal da Fraternidade, nosso guia e fonte de inspiração. É a alma da consagração salvista: sua obra de renovação da Igreja é a razão de existirmos."),
    ("Nossa Senhora de Pentecostes", "patrono", "17 de setembro",
     "A Virgem Maria, Mãe de Deus, modelo e proteção da vida consagrada. Sob o título de Nossa Senhora de Pentecostes é a padroeira do Instituto, e seu ícone é venerado em todas as nossas comunidades."),
    ("São José", "patrono", "19 de março",
     "Modelo para toda a nossa vida. Pela confiança e pela fé respondeu à fidelidade de Deus e foi fiel até a morte à sua humilde paternidade. Vamos a ele como nosso Pai e Protetor."),
    ("São Miguel Arcanjo", "patrono", "29 de setembro",
     "Nosso Defensor Celestial, eleito para proteger nossas comunidades e missionários em todo tempo e lugar."),
    ("São Tomás de Aquino", "baluarte", "28 de janeiro", "Intercessor dos estudos."),
    ("Santa Escolástica", "baluarte", "10 de fevereiro", ""),
    ("São Bento", "baluarte", "11 de julho", ""),
    ("São João Maria Vianney", "baluarte", "4 de agosto", ""),
    ("Santa Teresinha do Menino Jesus", "baluarte", "1º de outubro", ""),
    ("São Francisco Xavier", "baluarte", "3 de dezembro", ""),
]
santos_out = [{"nome": n, "tipo": t, "festa": f, "descricao": d, "ordem": i} for i, (n, t, f, d) in enumerate(santos)]

# ---------------------------------------------------------------- missões (dados de 2019: importadas como rascunho)
M = lambda nome, tipo, pais, diocese, cidade, estado, inicio, resp, lat, lng, resumo="": dict(
    nome=nome, tipo=tipo, pais=pais, diocese=diocese, cidade=cidade, estado=estado, inicio=inicio,
    responsaveisTexto=resp, latitude=lat, longitude=lng, resumo=resumo)
missoes = [
    M("Paróquia Nossa Senhora de Pentecostes", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo (Grajaú)", "SP", "fev/2000", "Pe. Francisco de Assis, sjs", -23.78, -46.69, "Nossa primeira missão estável."),
    M("Paróquia Santa Cecília", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "fev/2012", "Pe. Ronaldo Maria, sjs", -23.77, -46.70),
    M("Centro de Promoção Social Bororé", "obra-social", "brasil", "Diocese de Santo Amaro", "São Paulo (Grajaú)", "SP", "fev/2000", "Pe. Fábio Muniz Alves, sjs", -23.79, -46.68, "Acolhe cerca de 450 crianças, adolescentes e jovens em situação de risco social."),
    M("Seminário Maior Nossa Senhora de Pentecostes", "casa-de-formacao", "brasil", "Diocese de Santo Amaro", "São Paulo (Parelheiros)", "SP", "17/09/1994", "Pe. Helder Pio, sjs (reitor); Pe. Wendel Xavier, sjs; Pe. Micael de Moraes, sjs", -23.83, -46.72, "Casa de formação e seminário maior, onde os Institutos foram erigidos."),
    M("Noviciado Salvista", "casa-de-formacao", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "", "Pe. Martinho, sjs (mestre de noviços)", -23.83, -46.72),
    M("Paróquia Santa Bárbara", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "abr/2001", "Pe. João Evangelista, sjs; Pe. Henrique Maria, sjs", -23.80, -46.71),
    M("Paróquia São Cristóvão", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "abr/2003", "Pe. Carlos Cavalieri, sjs; Pe. Myguel Tostes, sjs", -23.81, -46.70),
    M("Paróquia São Vicente de Paulo", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "mar/2004", "Pe. Luciano Oliveira, sjs; Pe. Luciano Resende, sjs", -23.76, -46.69),
    M("Paróquia Santa Cruz", "paroquia", "brasil", "Diocese de Santo Amaro", "São Paulo", "SP", "abr/2005", "Pe. Claudionor, sjs; Pe. Fábio Francisco, sjs", -23.82, -46.69),
    M("Paróquia Mãe de Jesus", "paroquia", "brasil", "Arquidiocese de São Paulo", "São Paulo (Ipiranga)", "SP", "fev/2007", "Pe. Sandro do Nascimento, sjs; Pe. Mariano Rodrigo, sjs", -23.60, -46.60),
    M("Casa Apostólica Pe. Gilberto Maria Defina", "casa-apostolica", "brasil", "Arquidiocese de São Paulo", "São Paulo", "SP", "", "Casa do Prior Geral", -23.59, -46.61),
    M("Paróquia Nossa Senhora Aparecida", "paroquia", "brasil", "Diocese de Dourados", "Douradina", "MS", "fev/2004", "Pe. Odair José, sjs; Pe. Martinho Alves", -22.04, -54.61, "Nossa primeira missão fora da diocese de nascimento."),
    M("Paróquia São Francisco de Assis", "paroquia", "brasil", "Arquidiocese de Belém do Pará", "Belém", "PA", "jan/2012", "Pe. Rogério Rodrigues, sjs; Pe. Paulo da Eucaristia, sjs", -1.45, -48.49, "Nossa primeira missão na região Norte."),
    M("Paróquia da Natividade", "paroquia", "brasil", "Arquidiocese de Belém do Pará", "Belém", "PA", "", "Pe. Osmar, sjs; Pe. João da Cruz, sjs", -1.43, -48.46),
    M("Paroisse Sainte-Anne", "paroquia", "franca", "Diocese de Fréjus-Toulon", "Six-Fours-les-Plages", "", "jun/2005", "Pe. Ronicés Geber, sjs; Pe. Augusto Zanin, sjs; Pe. Luciano Oliveira, sjs; Pe. Rafael Maria, sjs", 43.09, 5.84, "Primeira missão salvista na Europa."),
    M("Parrocchia San Giovanni Battista", "paroquia", "italia", "Diocese de Lamezia Terme", "Gizzeria", "", "out/2006", "Pe. Paulo Mariano, sjs; Pe. Moisés Francisco, sjs; Pe. Paulo da Trindade, sjs", 38.98, 16.20),
    M("Paróquia São Sebastião e Centro Social", "paroquia", "portugal", "Diocese de Coimbra", "Meãs do Campo", "", "fev/2007", "Pe. Francisco de Moraes, sjs", 40.21, -8.62),
    M("Paróquia Nossa Senhora da Assunção", "paroquia", "portugal", "Diocese de Coimbra", "Tentúgal", "", "fev/2007", "Pe. Francisco de Moraes, sjs", 40.24, -8.60),
    M("Paróquia Nossa Senhora da Conceição", "paroquia", "portugal", "Diocese de Coimbra", "Lamarosa", "", "fev/2007", "Pe. Lucas Pio, sjs", 40.28, -8.60),
    M("Paróquia São Silvestre", "paroquia", "portugal", "Diocese de Coimbra", "São Silvestre", "", "fev/2007", "Pe. Lucas Pio, sjs", 40.23, -8.53),
    M("Paróquia São Martinho", "paroquia", "portugal", "Diocese de Coimbra", "São Martinho de Árvore", "", "fev/2007", "Pe. Lucas Pio, sjs", 40.25, -8.53),
    M("Paróquia Nossa Senhora do Pranto e Centro Social", "paroquia", "portugal", "Diocese de Coimbra", "Arazede", "", "nov/2011", "Pe. Fábio Muniz, sjs", 40.29, -8.65),
]

# ---------------------------------------------------------------- configurações e horários
configuracao = {
    "nomeSite": "Fraternidade Jesus Salvador",
    "lema": "No mínimo, devemos dar a Deus o máximo.",
    "descricao": "Padres, irmãos, irmãs e leigos que vivem para o louvor de Deus e levam a salvação de Jesus a quem mais precisa.",
    "valorSugeridoApadrinhamento": 25,
    "locais": [
        {"nome": "Instituto Missionário Servos de Jesus Salvador", "endereco": "Rua Antônio Marcondes Boêta, 590", "bairro": "Jardim Aladim (Parelheiros)",
         "cidade": "São Paulo/SP", "cep": "04883-210", "telefone": "(11) 5920-3920", "email": "salvistas@salvistas.com.br"},
        {"nome": "Instituto Missionário Servas de Jesus Salvador", "endereco": "Estrada do Barro Branco, 791/559", "bairro": "Jardim Lucélia",
         "cidade": "São Paulo/SP", "cep": "04852-320", "telefone": "(11) 5528-0571", "email": "irmas_sjs@hotmail.com"},
    ],
    "redes": [
        {"rede": "facebook", "url": "https://www.facebook.com/salvistas/"},
        {"rede": "youtube", "url": "https://www.youtube.com/user/salvistas"},
    ],
    "contas": [
        {"destino": "seminario", "banco": "Bradesco", "agencia": "2720-0", "conta": "6141-7"},
        {"destino": "seminario", "banco": "Banco do Brasil", "agencia": "1818-X", "conta": "12131-2"},
        {"destino": "seminario", "banco": "Itaú", "agencia": "0767", "conta": "40366-0"},
        {"destino": "seminario", "banco": "Caixa Econômica Federal", "agencia": "4139", "conta": "87-8", "operacao": "003"},
        {"destino": "convento", "banco": "Itaú", "agencia": "0360", "conta": "56926-3"},
        {"destino": "convento", "banco": "Bradesco", "agencia": "1480-0", "conta": "31208-8"},
    ],
}
horarios = [
    {"titulo": "Santa Missa", "quando": "Domingo", "hora": "9h", "local": "Seminário Nossa Senhora de Pentecostes", "ordem": 1},
    {"titulo": "Missa com orações por cura e libertação", "quando": "2º sábado do mês", "hora": "14h30", "local": "Seminário Nossa Senhora de Pentecostes", "ordem": 2},
]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"categorias": [{"nome": n, "slug": s, "descricao": d} for n, s, d, _ in CATEGORIAS],
           "posts": posts_out, "oracoes": oracoes, "santos": santos_out, "missoes": missoes,
           "configuracao": configuracao, "horarios": horarios},
          open(OUT, "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(posts_out), "posts", Counter(p["categoria"] for p in posts_out), "|", len(oracoes), "orações |",
      len(santos_out), "santos |", len(missoes), "missões")
print("orações:", [o["titulo"] for o in oracoes])
