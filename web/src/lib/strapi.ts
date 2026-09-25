// Cliente mínimo da API do Strapi 5. As páginas são geradas a cada visita; as respostas
// ficam num cache curto em memória (CACHE_SEGUNDOS, padrão 60) para o site responder rápido
// e o que for publicado no painel aparecer em até um minuto.

// Variáveis lidas na hora (process.env), não no build: o mesmo build serve qualquer ambiente.
const env = (k: string): string | undefined => process.env[k] ?? (import.meta.env as Record<string, string | undefined>)[k];

const STRAPI_URL = (env('STRAPI_URL') ?? 'http://localhost:1337').replace(/\/$/, '');
const PUBLIC_STRAPI_URL = (env('PUBLIC_STRAPI_URL') ?? STRAPI_URL).replace(/\/$/, '');
const TOKEN = env('STRAPI_TOKEN');
const TTL = Number(env('CACHE_SEGUNDOS') ?? 60) * 1000;

export type Media = {
  url: string;
  alternativeText: string | null;
  width: number | null;
  height: number | null;
  hash?: string;
  formats?: Record<string, { url: string; width: number; height: number }>;
};

export type Block = { type: string; [k: string]: any };

export type Categoria = { documentId: string; nome: string; slug: string; descricao?: string };

export type Post = {
  documentId: string;
  titulo: string;
  slug: string;
  resumo: string | null;
  data: string;
  capa: Media | null;
  conteudo: Block[];
  categoria: Categoria | null;
};

export type Oracao = {
  documentId: string;
  titulo: string;
  slug: string;
  intencao: string | null;
  introducao: string | null;
  texto: Block[];
  ordem: number;
};

export type Santo = { nome: string; slug: string; tipo: 'patrono' | 'baluarte'; festa: string; descricao: string | null; ordem: number };

export type Missao = {
  documentId: string;
  nome: string;
  slug: string;
  tipo: string;
  pais: 'brasil' | 'franca' | 'italia' | 'portugal' | 'outro';
  diocese: string | null;
  cidade: string | null;
  estado: string | null;
  inicio: string | null;
  resumo: string | null;
  responsaveisTexto: string | null;
  ordem: number;
};

export type Horario = { titulo: string; quando: string; hora: string | null; local: string | null; observacao: string | null };

export type Local = { nome: string; endereco?: string; bairro?: string; cidade?: string; cep?: string; telefone?: string; email?: string; mapaUrl?: string };

export type Configuracao = {
  nomeSite: string;
  lema: string;
  descricao: string | null;
  locais: Local[];
  redes: { rede: string; url: string; rotulo?: string }[];
  pixChave: string | null;
  pixFavorecido: string | null;
  valorSugeridoApadrinhamento: number | null;
  contas: { destino: 'seminario' | 'convento'; banco: string; agencia?: string; conta?: string; operacao?: string }[];
};

const cache = new Map<string, { em: number; dados: unknown }>();

async function get<T>(path: string, params: Record<string, string> = {}): Promise<T | null> {
  const url = new URL(`${STRAPI_URL}/api/${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const chave = url.toString();
  const guardado = cache.get(chave);
  if (guardado && Date.now() - guardado.em < TTL) return guardado.dados as T | null;

  try {
    const res = await fetch(url, { headers: TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {} });
    if (res.status === 404) {
      cache.set(chave, { em: Date.now(), dados: null });
      return null;
    }
    if (!res.ok) throw new Error(`${res.status} ${url}`);
    const dados = ((await res.json()) as { data: T }).data;
    cache.set(chave, { em: Date.now(), dados });
    return dados;
  } catch (e) {
    // CMS fora do ar: serve a última versão conhecida; sem ela, a seção sai vazia em vez de quebrar a página.
    console.warn(`[strapi] ${(e as Error).message}`);
    return (guardado?.dados as T | undefined) ?? null;
  }
}

export const mediaUrl = (m?: { url: string } | null) =>
  !m ? undefined : m.url.startsWith('http') ? m.url : `${PUBLIC_STRAPI_URL}${m.url}`;

export const getPosts = async (limit = 100) =>
  (await get<Post[]>('posts', {
    'sort[0]': 'data:desc',
    'pagination[pageSize]': String(limit),
    'populate[capa]': 'true',
    'populate[categoria]': 'true',
  })) ?? [];

const primeiro = <T>(lista: T[] | null) => lista?.[0] ?? null;

export const getPost = async (slug: string) =>
  primeiro(await get<Post[]>('posts', { 'filters[slug][$eq]': slug, 'populate[capa]': 'true', 'populate[categoria]': 'true' }));

export const getPostsDaCategoria = async (slug: string, limit = 100) =>
  (await get<Post[]>('posts', {
    'filters[categoria][slug][$eq]': slug,
    'sort[0]': 'data:desc',
    'pagination[pageSize]': String(limit),
    'populate[capa]': 'true',
    'populate[categoria]': 'true',
  })) ?? [];

export const getCategoria = async (slug: string) => primeiro(await get<Categoria[]>('categorias', { 'filters[slug][$eq]': slug }));

export const getOracao = async (slug: string) => primeiro(await get<Oracao[]>('oracoes', { 'filters[slug][$eq]': slug }));

export const getCategorias = async () => (await get<Categoria[]>('categorias', { 'sort[0]': 'nome:asc' })) ?? [];

export const getOracoes = async () =>
  (await get<Oracao[]>('oracoes', { 'sort[0]': 'ordem:asc', 'pagination[pageSize]': '100' })) ?? [];

export const getSantos = async () =>
  (await get<Santo[]>('santos', { 'sort[0]': 'ordem:asc', 'pagination[pageSize]': '100' })) ?? [];

// STRAPI_RASCUNHOS=true (só em desenvolvimento) mostra missões ainda em rascunho, para revisar antes de publicar.
const rascunhos: Record<string, string> = env('STRAPI_RASCUNHOS') === 'true' ? { status: 'draft' } : {};

export const getMissoes = async () =>
  (await get<Missao[]>('missoes', { 'sort[0]': 'ordem:asc', 'sort[1]': 'nome:asc', 'pagination[pageSize]': '200', 'filters[ativa][$eq]': 'true', ...rascunhos })) ?? [];

export const getHorarios = async () => (await get<Horario[]>('horarios', { 'sort[0]': 'ordem:asc' })) ?? [];

export const getConfiguracao = async () =>
  get<Configuracao>('configuracao', { 'populate[locais]': 'true', 'populate[redes]': 'true', 'populate[contas]': 'true' });

export const formEndpoint = `${PUBLIC_STRAPI_URL}/api/mensagens`;

export const dataLonga = (iso: string) =>
  new Date(`${iso}T12:00:00`).toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' });
