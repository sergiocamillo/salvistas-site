import type { Core } from '@strapi/strapi';

// Leitura pública de todo o conteúdo do site. Mensagens: o público só pode enviar.
const PUBLIC_READ = [
  'post', 'categoria', 'autor', 'pagina', 'missao', 'pessoa', 'oracao', 'santo', 'horario',
];
const PUBLIC_SINGLE = ['inicio', 'configuracao'];

async function grantPublicPermissions(strapi: Core.Strapi) {
  const role = await strapi.db
    .query('plugin::users-permissions.role')
    .findOne({ where: { type: 'public' } });
  if (!role) return;

  const actions = [
    ...PUBLIC_READ.flatMap((t) => [`api::${t}.${t}.find`, `api::${t}.${t}.findOne`]),
    ...PUBLIC_SINGLE.map((t) => `api::${t}.${t}.find`),
    'api::mensagem.mensagem.create',
  ];

  for (const action of actions) {
    const exists = await strapi.db
      .query('plugin::users-permissions.permission')
      .findOne({ where: { action, role: role.id } });
    if (!exists) {
      await strapi.db
        .query('plugin::users-permissions.permission')
        .create({ data: { action, role: role.id } });
    }
  }
}

export default {
  register() {},

  async bootstrap({ strapi }: { strapi: Core.Strapi }) {
    await grantPublicPermissions(strapi);
  },
};
