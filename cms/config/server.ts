import type { Core } from '@strapi/strapi';

const config = ({ env }: Core.Config.Shared.ConfigParams): Core.Config.Server => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
  // Endereço público (ex.: https://cms.salvistas.com.br). Necessário atrás do proxy do Railway.
  url: env('PUBLIC_URL', ''),
  proxy: { koa: env.bool('IS_PROXIED', env('NODE_ENV') === 'production') },
  app: {
    keys: env.array('APP_KEYS')!,
  },
  webhooks: {
    populateRelations: env.bool('WEBHOOKS_POPULATE_RELATIONS', false),
  },
});

export default config;
