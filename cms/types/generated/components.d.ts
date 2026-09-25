import type { Schema, Struct } from '@strapi/strapi';

export interface BlocosChamada extends Struct.ComponentSchema {
  collectionName: 'components_blocos_chamada';
  info: {
    displayName: 'Chamada';
    icon: 'cursor';
  };
  attributes: {
    links: Schema.Attribute.Component<'shared.link', true>;
    texto: Schema.Attribute.Text;
    titulo: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface BlocosCitacao extends Struct.ComponentSchema {
  collectionName: 'components_blocos_citacao';
  info: {
    displayName: 'Cita\u00E7\u00E3o';
    icon: 'quote';
  };
  attributes: {
    autor: Schema.Attribute.String;
    fonte: Schema.Attribute.String;
    texto: Schema.Attribute.Text & Schema.Attribute.Required;
  };
}

export interface BlocosGaleria extends Struct.ComponentSchema {
  collectionName: 'components_blocos_galeria';
  info: {
    displayName: 'Galeria';
    icon: 'apps';
  };
  attributes: {
    imagens: Schema.Attribute.Media<'images', true>;
    titulo: Schema.Attribute.String;
  };
}

export interface BlocosImagem extends Struct.ComponentSchema {
  collectionName: 'components_blocos_imagem';
  info: {
    displayName: 'Imagem';
    icon: 'picture';
  };
  attributes: {
    imagem: Schema.Attribute.Media<'images'> & Schema.Attribute.Required;
    largura: Schema.Attribute.Enumeration<['texto', 'larga', 'tela-cheia']> &
      Schema.Attribute.DefaultTo<'larga'>;
    legenda: Schema.Attribute.String;
  };
}

export interface BlocosOracoes extends Struct.ComponentSchema {
  collectionName: 'components_blocos_oracoes';
  info: {
    displayName: 'Ora\u00E7\u00F5es';
    icon: 'heart';
  };
  attributes: {
    oracoes: Schema.Attribute.Relation<'oneToMany', 'api::oracao.oracao'>;
    titulo: Schema.Attribute.String;
  };
}

export interface BlocosPessoas extends Struct.ComponentSchema {
  collectionName: 'components_blocos_pessoas';
  info: {
    displayName: 'Pessoas';
    icon: 'user';
  };
  attributes: {
    pessoas: Schema.Attribute.Relation<'oneToMany', 'api::pessoa.pessoa'>;
    titulo: Schema.Attribute.String;
  };
}

export interface BlocosTexto extends Struct.ComponentSchema {
  collectionName: 'components_blocos_texto';
  info: {
    displayName: 'Texto';
    icon: 'feather';
  };
  attributes: {
    conteudo: Schema.Attribute.Blocks;
    titulo: Schema.Attribute.String;
  };
}

export interface BlocosVideo extends Struct.ComponentSchema {
  collectionName: 'components_blocos_video';
  info: {
    displayName: 'V\u00EDdeo';
    icon: 'play';
  };
  attributes: {
    titulo: Schema.Attribute.String;
    youtubeUrl: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface SharedContaBancaria extends Struct.ComponentSchema {
  collectionName: 'components_shared_conta_bancaria';
  info: {
    displayName: 'Conta banc\u00E1ria';
    icon: 'bank';
  };
  attributes: {
    agencia: Schema.Attribute.String;
    banco: Schema.Attribute.String & Schema.Attribute.Required;
    conta: Schema.Attribute.String;
    destino: Schema.Attribute.Enumeration<['seminario', 'convento']> &
      Schema.Attribute.DefaultTo<'seminario'>;
    operacao: Schema.Attribute.String;
  };
}

export interface SharedHero extends Struct.ComponentSchema {
  collectionName: 'components_shared_hero';
  info: {
    displayName: 'Hero';
    icon: 'picture';
  };
  attributes: {
    chamadas: Schema.Attribute.Component<'shared.link', true>;
    imagem: Schema.Attribute.Media<'images'>;
    sobretitulo: Schema.Attribute.String;
    subtitulo: Schema.Attribute.Text;
    titulo: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface SharedLink extends Struct.ComponentSchema {
  collectionName: 'components_shared_link';
  info: {
    displayName: 'Link';
    icon: 'link';
  };
  attributes: {
    label: Schema.Attribute.String & Schema.Attribute.Required;
    url: Schema.Attribute.String & Schema.Attribute.Required;
    variante: Schema.Attribute.Enumeration<
      ['principal', 'secundario', 'texto']
    > &
      Schema.Attribute.DefaultTo<'principal'>;
  };
}

export interface SharedLocal extends Struct.ComponentSchema {
  collectionName: 'components_shared_local';
  info: {
    displayName: 'Local';
    icon: 'pinMap';
  };
  attributes: {
    bairro: Schema.Attribute.String;
    cep: Schema.Attribute.String;
    cidade: Schema.Attribute.String;
    email: Schema.Attribute.Email;
    endereco: Schema.Attribute.String;
    mapaUrl: Schema.Attribute.String;
    nome: Schema.Attribute.String & Schema.Attribute.Required;
    telefone: Schema.Attribute.String;
  };
}

export interface SharedRedeSocial extends Struct.ComponentSchema {
  collectionName: 'components_shared_rede_social';
  info: {
    displayName: 'Rede social';
    icon: 'earth';
  };
  attributes: {
    rede: Schema.Attribute.Enumeration<
      [
        'instagram',
        'facebook',
        'youtube',
        'whatsapp',
        'tiktok',
        'spotify',
        'outra',
      ]
    > &
      Schema.Attribute.Required;
    rotulo: Schema.Attribute.String;
    url: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface SharedSeo extends Struct.ComponentSchema {
  collectionName: 'components_shared_seo';
  info: {
    displayName: 'SEO';
    icon: 'search';
  };
  attributes: {
    metaDescription: Schema.Attribute.Text &
      Schema.Attribute.SetMinMaxLength<{
        maxLength: 170;
      }>;
    metaTitle: Schema.Attribute.String &
      Schema.Attribute.SetMinMaxLength<{
        maxLength: 70;
      }>;
    shareImage: Schema.Attribute.Media<'images'>;
  };
}

declare module '@strapi/strapi' {
  export namespace Public {
    export interface ComponentSchemas {
      'blocos.chamada': BlocosChamada;
      'blocos.citacao': BlocosCitacao;
      'blocos.galeria': BlocosGaleria;
      'blocos.imagem': BlocosImagem;
      'blocos.oracoes': BlocosOracoes;
      'blocos.pessoas': BlocosPessoas;
      'blocos.texto': BlocosTexto;
      'blocos.video': BlocosVideo;
      'shared.conta-bancaria': SharedContaBancaria;
      'shared.hero': SharedHero;
      'shared.link': SharedLink;
      'shared.local': SharedLocal;
      'shared.rede-social': SharedRedeSocial;
      'shared.seo': SharedSeo;
    }
  }
}
