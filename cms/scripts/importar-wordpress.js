/**
 * Importa data/importacao.json (gerado por conteudo-original/exportar_strapi.py) para o Strapi.
 *
 *   npm run importar
 *
 * Pode rodar mais de uma vez: pula o que já existe (pelo slug) e reaproveita imagens já enviadas.
 * Posts "migrar" entram publicados; posts "revisar" e todas as missões entram como rascunho.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { compileStrapi, createStrapi } = require('@strapi/strapi');

const DATA = path.join(__dirname, '..', 'data', 'importacao.json');
const CACHE = path.join(__dirname, '..', 'data', '.media-cache.json');

const MIME = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp' };

const slugify = (t) =>
  t.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

async function main() {
  const data = JSON.parse(fs.readFileSync(DATA, 'utf8'));
  const cache = fs.existsSync(CACHE) ? JSON.parse(fs.readFileSync(CACHE, 'utf8')) : {};

  const app = await createStrapi(await compileStrapi()).load();
  app.log.level = 'error';
  const docs = (uid) => app.documents(uid);
  const upload = app.plugin('upload').service('upload');

  async function media(url, alt = '') {
    if (!url) return null;
    if (cache[url]) {
      const f = await app.db.query('plugin::upload.file').findOne({ where: { id: cache[url] } });
      if (f) return f;
    }
    let res;
    try {
      res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    } catch {
      return null;
    }
    if (!res.ok) {
      console.warn('  imagem indisponível', res.status, url);
      return null;
    }
    const buf = Buffer.from(await res.arrayBuffer());
    const ext = (path.extname(new URL(url).pathname) || '.jpg').toLowerCase();
    const name = decodeURIComponent(path.basename(new URL(url).pathname));
    const tmp = path.join(os.tmpdir(), `wp-${Date.now()}-${Math.random().toString(36).slice(2)}${ext}`);
    fs.writeFileSync(tmp, buf);
    try {
      const [file] = await upload.upload({
        data: { fileInfo: { name, alternativeText: alt || null } },
        files: { filepath: tmp, originalFilename: name, mimetype: MIME[ext] || 'image/jpeg', size: buf.length },
      });
      cache[url] = file.id;
      fs.writeFileSync(CACHE, JSON.stringify(cache, null, 1));
      return file;
    } finally {
      fs.rmSync(tmp, { force: true });
    }
  }

  // Troca marcadores {type:image, src} e {type:video} por blocos válidos do Strapi.
  async function resolveBlocks(blocks) {
    const out = [];
    for (const b of blocks || []) {
      if (b.type === 'image') {
        const f = await media(b.src, b.alt);
        if (!f) continue;
        out.push({
          type: 'image',
          image: {
            name: f.name, alternativeText: f.alternativeText || '', url: f.url, caption: f.caption || null,
            width: f.width, height: f.height, formats: f.formats, hash: f.hash, ext: f.ext, mime: f.mime,
            size: f.size, previewUrl: f.previewUrl || null, provider: f.provider,
            createdAt: f.createdAt, updatedAt: f.updatedAt,
          },
          children: [{ type: 'text', text: '' }],
        });
      } else if (b.type === 'video') {
        const url = b.src.startsWith('//') ? `https:${b.src}` : b.src;
        out.push({ type: 'paragraph', children: [{ type: 'link', url, children: [{ type: 'text', text: 'Assista ao vídeo' }] }] });
      } else {
        out.push(b);
      }
    }
    return out;
  }

  async function exists(uid, slug) {
    return (await docs(uid).findFirst({ filters: { slug }, status: 'draft' })) != null;
  }

  // ---------- categorias
  const cats = {};
  for (const c of data.categorias) {
    let doc = await docs('api::categoria.categoria').findFirst({ filters: { slug: c.slug } });
    if (!doc) doc = await docs('api::categoria.categoria').create({ data: c });
    cats[c.slug] = doc.documentId;
  }
  console.log('categorias:', Object.keys(cats).length);

  // ---------- posts
  let n = 0;
  for (const p of data.posts) {
    if (await exists('api::post.post', p.slug)) continue;
    const capa = await media(p.capa);
    await docs('api::post.post').create({
      data: {
        titulo: p.titulo, slug: p.slug, data: p.data, resumo: p.resumo,
        conteudo: await resolveBlocks(p.conteudo), capa: capa ? capa.id : null,
        categoria: cats[p.categoria], urlAntiga: p.urlAntiga,
      },
      ...(p.publicar ? { status: 'published' } : {}),
    });
    n++;
    console.log(`  post ${p.publicar ? '✓' : '·'} ${p.titulo}`);
  }
  console.log('posts novos:', n);

  // ---------- orações
  for (const o of data.oracoes) {
    if (await exists('api::oracao.oracao', o.slug)) continue;
    await docs('api::oracao.oracao').create({ data: { ...o, texto: await resolveBlocks(o.texto) }, status: 'published' });
  }
  console.log('orações:', data.oracoes.length);

  // ---------- santos
  for (const s of data.santos) {
    const found = await docs('api::santo.santo').findFirst({ filters: { nome: s.nome } });
    if (!found) await docs('api::santo.santo').create({ data: { ...s, slug: slugify(s.nome) } });
  }
  console.log('santos:', data.santos.length);

  // ---------- missões (rascunho: dados de 2019, a Fraternidade confirma antes de publicar)
  for (const m of data.missoes) {
    const found = await docs('api::missao.missao').findFirst({ filters: { nome: m.nome }, status: 'draft' });
    if (!found) await docs('api::missao.missao').create({ data: { ...m, slug: slugify(`${m.nome}-${m.cidade}`) } });
  }
  console.log('missões (rascunho):', data.missoes.length);

  // ---------- horários
  for (const h of data.horarios) {
    const found = await docs('api::horario.horario').findFirst({ filters: { titulo: h.titulo } });
    if (!found) await docs('api::horario.horario').create({ data: h });
  }

  // ---------- configurações (tipo único)
  const cfg = await docs('api::configuracao.configuracao').findFirst();
  if (!cfg) {
    const root = path.join(__dirname, '..', '..', 'referencias');
    const local = async (file, alt) => {
      const p = path.join(root, file);
      if (!fs.existsSync(p)) return null;
      const [f] = await upload.upload({
        data: { fileInfo: { name: file, alternativeText: alt } },
        files: { filepath: p, originalFilename: file, mimetype: MIME[path.extname(p)] || 'image/png', size: fs.statSync(p).size },
      });
      return f.id;
    };
    await docs('api::configuracao.configuracao').create({
      data: {
        ...data.configuracao,
        logo: await local('logo-fjs-selo.png', 'Selo da Fraternidade Jesus Salvador'),
        brasao: await local('logo-imsjs-brasao.png', 'Brasão do Instituto Missionário Servos de Jesus Salvador'),
      },
    });
    console.log('configurações: criadas');
  }

  await app.destroy();
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
