# Publicar no Railway

Dois serviços no mesmo projeto, a partir do repositório `sergiocamillo/salvistas-site`:

| Serviço | Pasta (Root Directory) | O que é |
|---|---|---|
| **cms** | `/cms` | Strapi: painel, API, formulários, imagens |
| **salvistas-site** | `/web` | Site em Astro, gera as páginas a cada visita (cache de 60 s) |

Projeto `Salvistas` (d44a5493…). Em cada serviço: *Build Command* `npm run build`, *Start Command* `npm run start`,
*Watch Paths* `/cms/**` ou `/web/**` (um serviço só refaz o deploy quando a sua pasta muda). O site tem *Healthcheck* em `/`.
O Railway descontinuou o `railway.json`, então essas opções ficam nas configurações do serviço.

Banco: PostgreSQL remoto (no próprio Railway ou em outro provedor).

---

## 1. Banco de dados
- **No Railway:** no projeto, *+ New → Database → PostgreSQL*. A URL fica disponível como `${{Postgres.DATABASE_URL}}`.
- **Fora do Railway** (Neon, Supabase...): copie a URL de conexão. Normalmente precisa de SSL (veja o passo 2).

## 2. Serviço `cms` (Strapi)
1. *+ New → GitHub Repo →* `salvistas-site`.
2. *Settings → Source → Root Directory:* `/cms`.
3. *Settings → Networking → Generate Domain* (depois dá para trocar por `cms.salvistas.com.br`).
4. *Variables → Raw Editor:* cole o conteúdo de `cms/.env.railway` (arquivo local, fora do Git, com as chaves já geradas) e ajuste:
   - `DATABASE_URL=${{Postgres.DATABASE_URL}}` (Postgres do Railway) ou a URL do provedor externo.
   - Provedor externo: descomente `DATABASE_SSL=true` e `DATABASE_SSL_REJECT_UNAUTHORIZED=false`.
5. **Volume para as imagens** (sem ele, as imagens somem a cada deploy): clique com o botão direito no serviço *→ Attach Volume*, com o caminho de montagem **`/app/public/uploads`**.
6. Faça o deploy. O primeiro build leva alguns minutos (o painel é compilado).
7. Abra `https://<domínio-do-cms>/admin` e crie o usuário administrador.

## 3. Levar o conteúdo do computador para o Railway
No painel do Strapi publicado: *Settings → Transfer Tokens → Create new* (tipo **Push**, duração ilimitada). Copie o token e rode no computador, com o Strapi local parado:

```bash
cd cms && npx strapi transfer --to https://<domínio-do-cms>/admin --to-token <TOKEN>
```

Isso copia posts, orações, santos, missões, configurações **e as imagens**. Depois, apague o token no painel.

> O transfer substitui o conteúdo do destino. Rode antes de a equipe começar a publicar no painel.

## 4. Serviço `web` (Astro)
1. *+ New → GitHub Repo →* `salvistas-site` de novo.
2. *Root Directory:* `/web`.
3. *Variables:*

```
HOST=0.0.0.0
STRAPI_URL=http://${{cms.RAILWAY_PRIVATE_DOMAIN}}:1337
PUBLIC_STRAPI_URL=https://${{cms.RAILWAY_PUBLIC_DOMAIN}}
SITE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
CACHE_SEGUNDOS=60
```

   - `STRAPI_URL` usa a rede interna (mais rápida). Se o serviço do Strapi tiver outro nome, troque `cms`.
   - A porta 1337 vem de `PORT=1337`, já incluída no `.env.railway` do `cms`.
   - `PUBLIC_STRAPI_URL` é o endereço público: é por ele que o navegador carrega as imagens e envia os formulários.
4. *Generate Domain* e deploy.

## 5. Domínio
- `salvistas.com.br` → serviço **web**; `cms.salvistas.com.br` → serviço **cms** (*Settings → Networking → Custom Domain*, e crie os registros CNAME que o Railway mostrar).
- Depois atualize `PUBLIC_URL` (cms), `PUBLIC_STRAPI_URL` e `SITE_URL` (web) com os domínios finais.
- Antes de apontar o domínio: fazer os redirecionamentos 301 dos endereços antigos do WordPress.

## Como o conteúdo atualiza
A equipe publica no painel e o site mostra a mudança em até 60 segundos. Sem novo deploy, sem botão.

## Checklist depois do deploy
- [ ] `https://<web>/` abre com fotos e notícias
- [ ] Uma imagem de post abre (confirma `PUBLIC_STRAPI_URL` e o volume)
- [ ] Enviar o formulário de contato e ver a mensagem em *Content Manager → Mensagem*
- [ ] Missões ainda em rascunho **não** aparecem no site (bloqueio de rascunhos em produção)
- [ ] Fazer um deploy novo do `cms` e conferir que as imagens continuam lá (volume)
