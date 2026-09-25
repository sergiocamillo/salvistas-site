// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

// As páginas são geradas a cada visita (com cache curto em src/lib/strapi.ts),
// então o que a equipe publica no Strapi aparece no site sem novo deploy.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://salvistas.com.br',
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  security: { checkOrigin: true },
});
