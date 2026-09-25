import { factories } from '@strapi/strapi';

const CAMPOS = ['tipo', 'nome', 'email', 'telefone', 'cidade', 'mensagem', 'extra'] as const;

export default factories.createCoreController('api::mensagem.mensagem', () => ({
  // O público só envia. Aceita apenas os campos do formulário, descarta robôs
  // (campo "site" escondido no HTML) e sempre grava com status "nova".
  async create(ctx) {
    const body = (ctx.request.body as { data?: Record<string, unknown> })?.data ?? {};

    if (body.site) {
      ctx.status = 201;
      ctx.body = { ok: true };
      return;
    }

    const data: Record<string, unknown> = { status: 'nova' };
    for (const campo of CAMPOS) {
      if (body[campo] !== undefined) data[campo] = body[campo];
    }

    await strapi.documents('api::mensagem.mensagem').create({ data: data as never });

    ctx.status = 201;
    ctx.body = { ok: true };
  },
}));
