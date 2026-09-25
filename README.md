# Salvistas · novo site

Nova versão do site da Fraternidade Jesus Salvador (https://salvistas.com.br).

| Pasta | O que é |
|---|---|
| `cms/` | Strapi 5: painel, API, formulários e blog |
| `web/` | Site em Astro, gerado a partir da API do Strapi |
| `docs/` | Análise, triagem do blog e design package |
| `conteudo-original/` | Extração do WordPress atual e scripts de conversão |
| `referencias/` | Fotos do V Capítulo Geral 2026 e logos |

## Rodar localmente

```bash
# 1. CMS (http://localhost:1337/admin)
cd cms && npm install && npm run develop

# 2. Importar o conteúdo do WordPress (uma vez; pode repetir, ele pula o que já existe)
cd cms && npm run importar

# 3. Site (http://localhost:4321)
cd web && cp .env.example .env && npm install && npm run dev
```

Na primeira vez, o Strapi pede para criar o usuário administrador em `/admin`.

## Como o conteúdo flui
- A equipe publica no painel do Strapi. O site é estático: em produção, um webhook do Strapi dispara um novo build do Astro.
- Formulários (vocação, padrinho, pedido de oração, contato) gravam na coleção **Mensagem** do Strapi. O público só consegue enviar, nunca ler.
- Posts vindos da triagem com decisão "revisar" e as missões (dados de 2019) entram como **rascunho** até a Fraternidade confirmar.

## Regerar a importação
```bash
cd conteudo-original
python triagem.py            # classifica os 739 posts
python exportar_strapi.py    # gera cms/data/importacao.json (requer markdownify, beautifulsoup4)
```
