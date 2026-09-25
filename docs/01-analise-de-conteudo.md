# Salvistas: análise do site atual e proposta para o novo site

> Etapa 1 · extração e análise · 25/09/2026
> Fonte: https://salvistas.com.br (WordPress), extraído via REST API + artes do V Capítulo Geral (ago/2026)

---

## 1. O que foi extraído

| Item | Quantidade | Onde está |
|---|---|---|
| Páginas | 43 (15 vazias ou quase vazias) | `conteudo-original/paginas/*.md` + `_INDEX.md` |
| Posts do blog | 739 (2010 a 2019) | `conteudo-original/posts/<ano>/*.md` + `_INDEX.md` |
| Categorias | 13 (6 em uso) | `conteudo-original/raw/` |
| Tags | 3.415 (2.903 usadas uma vez só) | `conteudo-original/_tags-resumo.md` |
| Mídias na biblioteca | 86 | `conteudo-original/imagens/_INDEX.md` |
| Imagens das páginas | 67 baixadas | `conteudo-original/imagens/` |
| Artes do V Capítulo | 2 fotos em alta + 2 logos recortados | `referencias/` |

Dump bruto da API (JSON) guardado em `conteudo-original/raw/` para a migração ao Strapi.

---

## 2. Diagnóstico do site atual

### 2.1 Técnico
- **WordPress 7.0.2 + tema Betheme + Slider Revolution + Contact Form 7.** Pesado para o que entrega; o slider sozinho carrega muito JavaScript.
- **Usuário `admin` exposto** pela API pública (`/wp-json/wp/v2/users`). Facilita ataque de senha.
- **Post de spam publicado:** "Best Games to play in 2023" (`/best-games-to-play-in-2023/`), com data falsa de 2011, na categoria *Salvistas*, com links para `apkticket.com`. Sinal de que alguém já teve acesso ao painel ou a um plugin vulnerável. **Recomendo remover já, mesmo antes do novo site, e trocar as senhas.**
- Imagens antigas em baixa resolução (a maioria de 2012, vindas do Facebook, 300 a 700 px).
- Sem Instagram, sem WhatsApp, sem PIX. Só Facebook e YouTube linkados.

### 2.2 Conteúdo
- **Informações desatualizadas em pontos sensíveis:**
  - *Prior Geral*: Pe. Jucemar, "função que ocupará até 2026". O V Capítulo Geral (2026-2031) já aconteceu. **A página precisa do novo governo geral.**
  - *Nossas Missões*: lista de 2019, com nomes de padres e paróquias que provavelmente mudaram.
  - *O que fazemos* e *Histórico* se repetem e se contradizem em datas (1993 x 1994; ver 2.4).
- **Blog parado desde 2017** (último post real: jul/2017; um aviso de 2019). A home ainda dá a impressão de um site vivo, o que confunde.
- **~85% do blog é notícia replicada** (CNBB, Vaticano, agências católicas, Evangelho do dia). Conteúdo que envelhece e não é da Fraternidade. O conteúdo próprio (testemunhos, missões, ordenações, vida salvista) é minoria e está misturado.
- **Páginas duplicadas:** *Esfera Laical Salvista* x *Ordem Terceira (S.E.R.)*; *Apadrinhamento* x *Adote um Salvista* x *Formulário* x *Formulário Padrinho*; *Vocacional masculino* x *Instituto masculino*.
- **15 páginas vazias** que só servem de menu: Espiritualidade, Interatividade (Fotos, Vídeos, Links), Mural de Recados, Home etc.
- **Dados bancários soltos** em várias páginas, com agências diferentes para "Seminário" e "Convento". Difícil saber qual usar.
- **E-mails pessoais/antigos:** `irmas_sjs@hotmail.com`, `juventudesalvista@yahoo.com.br`, `livrariasalvista@gmail.com` misturados com `@salvistas.com.br`.
- **Tom da escrita:** reverente e bonito nos textos de espiritualidade, mas longo, com muito CAIXA ALTA, frases de 80+ palavras e jargão interno ("latrêutica", "cân 588,2") sem explicação para quem chega de fora.

### 2.3 O que é ouro (fica, com cuidado)
1. **O lema:** "No mínimo, devemos dar a Deus o máximo." Está pintado na fachada do seminário e aparece nas duas artes do Capítulo. É a assinatura da marca.
2. **A história de origem:** Pe. Gilberto ouviu jovens se dizerem "peixes fora d'água" na Igreja e fundou a Fraternidade. É humana, curta e memorável.
3. **O carisma em uma palavra: Louvor.** *Laus Dei* está no brasão.
4. **Nossa Senhora de Pentecostes:** devoção própria, inspirada ao fundador, com ícone original e texto de leitura do ícone muito bom. É um diferencial que nenhuma outra comunidade tem.
5. **A família completa:** Servos (padres e irmãos), Servas (irmãs), S.E.R. (leigos) e Juventude Salvista. A foto do Capítulo Geral mostra isso de um jeito que nenhum texto consegue.
6. **Presença em 4 países:** Brasil (SP, MS, PA), França, Itália e Portugal.
7. **Obra social:** Centro de Promoção Social Bororé, ~450 crianças e jovens no Grajaú.
8. **Orações próprias:** Providência Santíssima, Nossa Senhora de Pentecostes, São José. Muito procuradas por busca orgânica.

### 2.4 Inconsistências para a Fraternidade confirmar
- Fundação: *Quem somos* diz 1993 (Fraternidade); *Histórico* diz 17/09/1994 (Instituto). Proposta: "A Fraternidade nasceu em 1993; os Institutos foram erigidos em 17 de setembro de 1994."
- Aprovação como Instituto de Direito Diocesano: texto diz **10/11/2014**. Confirmar.
- Horários: "Domingo às 9h" e "2º sábado, 14h30, missa de cura e libertação". Ainda valem?
- Valor sugerido do apadrinhamento: **R$ 25/mês** (texto de 2020). Ainda vale?

---

## 3. Material novo: V Capítulo Geral 2026

| Arquivo | Uso sugerido |
|---|---|
| `referencias/foto-capitulo-geral-2026.jpg` (3600×2400) | Foto da família inteira. **Imagem principal do hero** e da seção "Quem somos". |
| `referencias/foto-capitulo-irmaos-2026.jpg` (3674×2450) | Só os Servos (padres e irmãos). Página do Instituto masculino e Vocação masculina. |
| `referencias/logo-fjs-selo.png` | Selo FJS (triângulo com a pomba + círculo dourado). **Logo principal do site.** |
| `referencias/logo-imsjs-brasao.png` | Brasão do Instituto Missionário Servos de Jesus Salvador (*Laus Dei*). Rodapé e página do instituto. |

Pendente: arte/brasão das **Servas** (irmãs), fotos das missões, foto do novo Prior Geral e conselho, e o ícone de Nossa Senhora de Pentecostes em alta resolução.

---

## 4. Decisão de conteúdo: o que fica, junta, reescreve ou sai

| Página atual | Decisão | Vai para |
|---|---|---|
| Histórico + Quem somos + O que fazemos | **Juntar e reescrever** | Quem somos |
| Carisma | Reescrever (curto) | Quem somos › Carisma |
| Nosso fundador | Manter, editar e dividir em blocos | Quem somos › Pe. Gilberto |
| Prior Geral | **Atualizar (V Capítulo)** e virar "Governo geral 2026-2031" | Quem somos › Governo |
| Nosso símbolo | Reescrever explicando o selo e o brasão | Quem somos › Símbolos |
| Nossas missões | **Atualizar** e virar mapa + fichas no CMS | Missões |
| NS de Pentecostes (3 páginas) | Juntar em 1 página rica, manter o texto do ícone | Espiritualidade |
| Patronos e baluartes | Manter, visual novo em cards | Espiritualidade |
| Orações (Providência, NS Pentecostes, São José) | Manter íntegras, uma página por oração | Espiritualidade › Orações |
| Instituto masculino / Vocacional masculino | Juntar | Família › Servos + Vocação |
| Instituto feminino / Vocacional feminino | Juntar | Família › Servas + Vocação |
| Ordem Terceira S.E.R. + Esfera Laical | Juntar | Família › Leigos (S.E.R.) |
| Juventude Salvista | Reescrever (mais curta, mais atual) | Família › Juventude |
| Manual do vocacionado (1.800 palavras) | Manter como PDF/página longa | Vocação |
| Apadrinhamento + Adote um Salvista + Formulários | **Juntar em uma página de doação** | Apoie |
| Providência Santíssima | Vira a abertura da página Apoie | Apoie |
| Contato + Como chegar + Nossas atividades | Juntar | Contato |
| Pedido de oração | Manter (formulário) | Contato › Pedido de oração |
| Livraria, Livros, Pedido do CD | **Confirmar se ainda existe** | Loja simples ou sai |
| Interatividade, Fotos, Vídeos, Links, Mural, Home, Espiritualidade (vazias) | **Sai** | 301 para a seção nova |
| Portfolio (3 galerias) | Sai (fotos vão para o blog se úteis) | · |

### Blog (739 posts)
Recomendação: **não migrar tudo.**
- **Migrar** (estimativa 40 a 80 posts): conteúdo próprio da Fraternidade, como testemunhos, ordenações, votos, missões, eventos salvistas, "Ser Irmã Salvista na França", "A minha vocação", "7 anos de adoração".
- **Não migrar:** notícias replicadas de CNBB/Vaticano/agências, "Evangelho do dia", intenções do Papa de 2011 a 2017. Envelheceram e não são da casa.
- **Apagar já:** o post de spam.
- **Tags:** zerar. O novo blog nasce com 6 a 8 categorias claras (Vida salvista, Missões, Vocação, Formação, Espiritualidade, Juventude, Eventos) e poucas tags.
- Todo post não migrado recebe **redirecionamento 301** para a categoria mais próxima, para não perder o Google.

A lista completa com data, categoria e tamanho está em `conteudo-original/posts/_INDEX.md`. Próximo passo: eu faço uma triagem automática por palavras-chave (salvista, sjs, ordenação, missão, votos, Bororé...) e a Fraternidade confirma a lista final.

---

## 5. Novo mapa do site

```
Início
Quem somos ........ história, carisma, Pe. Gilberto, governo geral 2026-2031, símbolos
Espiritualidade ... Nossa Senhora de Pentecostes, patronos e baluartes, orações
Família salvista .. Servos · Servas · Leigos (S.E.R.) · Juventude Salvista
Missões ........... mapa Brasil + Europa, uma ficha por missão, Centro Social Bororé
Vocação ........... "sinto um chamado": etapas, conversa com formador, manual   ← CTA 1
Apoie ............. Associação Providência Santíssima: padrinho/madrinha, PIX    ← CTA 2
Notícias .......... blog (Strapi)
Contato ........... endereços, horários de missa, como chegar, pedido de oração
```

A home conta a história em 6 movimentos curtos: lema → quem somos (foto do Capítulo) → a família → onde estamos → Nossa Senhora de Pentecostes → vocação e apoio → últimas notícias.

---

## 6. Nova comunicação

### 6.1 Tom de voz
- **Acolhedor e reverente, sem ser pesado.** Fala com "você", frases curtas, uma ideia por parágrafo.
- **Jargão só com tradução na mesma frase.** Ex.: "Somos um Instituto de Direito Diocesano, ou seja, reconhecido pela Igreja através do bispo de Santo Amaro."
- **Nada de CAIXA ALTA em texto corrido.** Títulos em versalete elegante, não em grito.
- **Citações das Constituições e do fundador em destaque**, como peças de valor, não enterradas em parágrafos longos.
- Os textos de oração e a leitura do ícone ficam **íntegros**: ali o público quer o texto original.

### 6.2 Exemplos de reescrita (rascunho para aprovação)

**Hero da home**
> *No mínimo, devemos dar a Deus o máximo.*
> Somos a Fraternidade Jesus Salvador: padres, irmãos, irmãs e leigos que vivem para o louvor de Deus e levam a salvação de Jesus a quem mais precisa.
> [Conheça a família salvista] [Sinto um chamado]

**Quem somos (abertura)**
> Tudo começou com uma conversa. Nos anos 90, o Pe. Gilberto Maria Defina ouviu muitos jovens dizerem que se sentiam "peixes fora d'água" na Igreja. Em 1993 ele fundou a Fraternidade Jesus Salvador para acolher esse chamado. Hoje somos uma família espalhada pelo Brasil, França, Itália e Portugal.

**Carisma**
> Nosso carisma é o louvor de Deus, em todas as suas formas, com a liturgia em primeiro lugar. Quem louva é transformado, e uma pessoa transformada transforma a comunidade à sua volta.

**Vocação**
> Sente que Deus está chamando você? Conte pra gente. Um formador vai conversar com você no seu tempo, sem pressa e sem compromisso.

**Apoie**
> Todo padre e toda irmã salvista foi formado com a ajuda de alguém. Com R$ 25 por mês, você se torna padrinho ou madrinha e sustenta a formação de quem vai servir a Igreja amanhã.

**Missões**
> Onde a Igreja nos chama, nós vamos. Hoje estamos em 4 países, com paróquias, casas de formação e uma obra social que acolhe cerca de 450 crianças e jovens no Grajaú, em São Paulo.

---

## 7. Direção visual (primeira proposta)

- **Paleta tirada das próprias fotos e logos:**
  - Marrom do hábito `#3F2620` (texto e fundos escuros)
  - Carmim do brasão `#8E1C1F` (acento, usado pouco)
  - Ouro litúrgico `#B8914A` (linhas, detalhes, nunca em blocos grandes)
  - Creme da fachada `#F4EEE3` (fundo principal, nunca branco puro)
  - Verde do gramado `#5E6B45` (apoio, raríssimo)
- **Tipografia:** display serifada clássica com cara de inscrição (ex.: *Cormorant Garamond*), versalete estilo romano para rótulos (*Cinzel*, que conversa com os logos) e uma sem serifa legível no corpo (ex.: *Figtree*). A escolha final vem na etapa de design.
- **Efeitos sutis (adaptando a skill 10k):** em vez do vídeo que roda com o scroll, o hero usa a **foto real do Capítulo** com entrada lenta (zoom quase imperceptível e revelação em camadas), **linhas douradas SVG que se desenham** ao rolar, títulos que surgem com leve fade, e uma **luz suave de Pentecostes** (partículas douradas em nível de sussurro) na seção de Nossa Senhora. Nada que distraia de uma leitura orante. Respeita "reduzir movimento" do sistema.
- A skill 10k segue valendo para: pesquisa de linguagem do público, texto sem clichê de IA, uma chamada principal por página, checklist de qualidade e teste em celular.

---

## 8. Arquitetura técnica proposta

| Camada | Escolha | Por quê |
|---|---|---|
| CMS | **Strapi 5** (headless) | Pedido do projeto. Painel simples para a comunidade publicar posts e editar páginas. |
| Banco | PostgreSQL | Padrão de produção do Strapi. |
| Front-end | **Astro** (recomendado) | Gera páginas estáticas muito rápidas, animações leves, ótimo SEO. Reconstrói sozinho quando alguém publica no Strapi (webhook). |
| Formulários | Salvos no Strapi + aviso por e-mail | Vocação, padrinho/madrinha, pedido de oração, contato. |
| Imagens | Upload do Strapi com versões otimizadas (WebP/AVIF) | |
| Repositório | `github.com/sergiocamillo/salvistas-site` | Monorepo: `/cms` (Strapi) e `/web` (Astro). |

**Observação honesta:** a skill 10k pede HTML puro sem framework. Com Strapi e blog isso não se sustenta, então mantemos da skill o padrão de design, texto e testes, e usamos Astro para o site consumir o CMS.

### Tipos de conteúdo no Strapi (rascunho)
- **Post** (título, resumo, capa, corpo rico, categoria, autor, data, SEO)
- **Categoria**, **Autor**
- **Página** (com blocos reutilizáveis: texto, citação, imagem, galeria, chamada, oração)
- **Missão** (país, diocese, nome, início, responsáveis, foto, coordenadas no mapa)
- **Pessoa** (nome, cargo, foto, bio curta) para governo geral e formadores
- **Oração** (título, texto, intenção)
- **Santo** (patrono/baluarte, data da festa, imagem)
- **Horário** (missas e atividades por local)
- **Configurações gerais** (contatos, redes, PIX, endereços) · tipo único
- **Envios de formulário** (vocacional, padrinho, oração, contato)

### Hospedagem (decidir depois)
Strapi precisa de um servidor Node sempre ligado + banco. Opções: Strapi Cloud, Railway/Render, ou um VPS (ex.: Hostinger). O site Astro pode ficar em Vercel, Netlify ou no mesmo VPS.

---

## 9. O que preciso da Fraternidade

1. **Governo geral eleito no V Capítulo** (Prior Geral, vigário e conselheiros, 2026-2031), com fotos.
2. **Lista atual das missões** (paróquias, dioceses, padres responsáveis).
3. **Horários de missa e atividades** que valem hoje.
4. **Chave PIX** oficial e se a Associação Providência Santíssima ainda envia boleto e jornal.
5. **E-mails oficiais** atuais (irmãs, juventude, vocacional, S.E.R.).
6. **Instagram** e demais redes ativas.
7. **Livraria/CD:** ainda existe?
8. **Material das Servas:** brasão/logo e fotos próprias.
9. **Ícone de Nossa Senhora de Pentecostes** em alta resolução.
10. Fotos recentes de missões, Centro Bororé, liturgias e juventude.

---

## 10. Próximos passos

1. Aprovação desta análise, do mapa do site e do tom de voz.
2. Triagem do blog (lista de posts a migrar).
3. Design package (paleta, tipos, layout da home, efeitos) no padrão da skill 10k.
4. Setup do monorepo: Strapi 5 + Astro, tipos de conteúdo, script de importação do WordPress.
5. Construção das páginas, migração de conteúdo, formulários.
6. Teste de qualidade (velocidade, celular, acessibilidade) e redirecionamentos 301.
7. Publicação.
