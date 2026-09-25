# Salvistas · novo site

Nova versão do site da Fraternidade Jesus Salvador (https://salvistas.com.br).

- **CMS:** Strapi 5 (`/cms`, a criar)
- **Site:** Astro (`/web`, a criar)

## Pastas

| Pasta | Conteúdo |
|---|---|
| `docs/` | Análise, decisões e design package |
| `conteudo-original/` | Extração do WordPress atual (páginas e posts em Markdown, dump JSON em `raw/`, imagens) |
| `referencias/` | Fotos do V Capítulo Geral 2026 e logos |

Para refazer a conversão do dump: `python converter.py` dentro de `conteudo-original/` (requer `markdownify` e `beautifulsoup4`).
