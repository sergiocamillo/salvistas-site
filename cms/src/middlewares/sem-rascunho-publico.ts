import type { Core } from '@strapi/strapi';

/**
 * O Strapi 5 devolve rascunhos para qualquer um que peça `?status=draft` na API.
 * Em produção, pedidos sem token de API sempre recebem só o conteúdo publicado.
 */
export default (_config: unknown, { strapi }: { strapi: Core.Strapi }) =>
  async (ctx: any, next: () => Promise<void>) => {
    const publico = ctx.path.startsWith('/api/') && !ctx.request.header.authorization;
    if (publico && strapi.config.get('environment') === 'production' && ctx.query?.status === 'draft') {
      ctx.query = { ...ctx.query, status: 'published' };
    }
    await next();
  };
