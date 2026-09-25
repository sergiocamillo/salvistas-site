// Renderiza o campo "blocks" do Strapi 5 em HTML.
import { mediaUrl, type Block } from './strapi';

const esc = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function inline(nodes: Block[] = []): string {
  return nodes
    .map((n) => {
      if (n.type === 'link') {
        const external = /^https?:/.test(n.url) && !n.url.includes('salvistas.com.br');
        return `<a href="${esc(n.url)}"${external ? ' target="_blank" rel="noopener"' : ''}>${inline(n.children)}</a>`;
      }
      let t = esc(n.text ?? '').replace(/\n/g, '<br>');
      if (n.code) t = `<code>${t}</code>`;
      if (n.bold) t = `<strong>${t}</strong>`;
      if (n.italic) t = `<em>${t}</em>`;
      if (n.underline) t = `<u>${t}</u>`;
      if (n.strikethrough) t = `<s>${t}</s>`;
      return t;
    })
    .join('');
}

export function renderBlocks(blocks: Block[] = []): string {
  return blocks
    .map((b) => {
      switch (b.type) {
        case 'heading':
          return `<h${b.level}>${inline(b.children)}</h${b.level}>`;
        case 'list': {
          const tag = b.format === 'ordered' ? 'ol' : 'ul';
          return `<${tag}>${b.children.map((li: Block) => `<li>${inline(li.children)}</li>`).join('')}</${tag}>`;
        }
        case 'quote':
          return `<blockquote><p>${inline(b.children)}</p></blockquote>`;
        case 'code':
          return `<pre><code>${inline(b.children)}</code></pre>`;
        case 'image': {
          const img = b.image;
          const src = mediaUrl(img.formats?.large ?? img);
          return `<figure><img src="${src}" alt="${esc(img.alternativeText ?? '')}" width="${img.width ?? ''}" height="${img.height ?? ''}" loading="lazy" decoding="async">${img.caption ? `<figcaption>${esc(img.caption)}</figcaption>` : ''}</figure>`;
        }
        default:
          return `<p>${inline(b.children)}</p>`;
      }
    })
    .join('\n');
}

export function plainText(blocks: Block[] = [], max = 200): string {
  const walk = (ns: Block[]): string => ns.map((n) => n.text ?? walk(n.children ?? [])).join(' ');
  const t = walk(blocks).replace(/\s+/g, ' ').trim();
  return t.length > max ? `${t.slice(0, max).replace(/\s\S*$/, '')}…` : t;
}
