# Design package · Fraternidade Jesus Salvador

## Premissa
O site é a casa da família salvista: acolhedor, orante, sem pressa. A foto real do V Capítulo Geral é a imagem principal; nada de vídeo gerado. Efeitos sutis, a serviço da leitura.

## Direção única
O mundo visual vem do próprio seminário: a fachada creme, o hábito marrom, o carmim do brasão e o ouro litúrgico dos selos. **Desvio assumido:** a skill 10k evita "fundo creme com serifa" como clichê, mas aqui esse é o material real da Fraternidade (fachada, ícone, brasão), então usamos esse mundo com tons tirados das fotos, sem o acento terracota do clichê.

## Assinatura
**O fio de ouro.** Os raios que descem da pomba no selo FJS viram:
- os raios dourados que se desenham atrás do lema, no topo da home;
- um fio vertical que se desenha entre as seções e termina numa pequena chama;
- a linha do tempo da página História, que acompanha a rolagem.

## Paleta (tokens em `web/src/styles/global.css`)
| Token | Hex | Uso |
|---|---|---|
| `--creme` | `#f4ede1` | Fundo principal (nunca branco puro) |
| `--creme-2` | `#ebe1cf` | Seções alternadas |
| `--marrom` | `#3a231d` | Texto (12,5:1 sobre creme) |
| `--noite` | `#2b1a15` | Seções escuras (nunca preto puro) |
| `--carmim` | `#8d1c20` | Acento raro: botão Apoie, ênfases, foco |
| `--ouro` | `#a98241` | Só decoração (linhas, raios) |
| `--ouro-texto` | `#7a5c2a` | Rótulos pequenos (5,3:1) |
| `--ouro-claro` | `#d8bd85` | Ouro sobre fundo escuro (9,1:1) |

## Tipografia
- **Cormorant Garamond** (display, títulos, orações, citações), com algarismos alinhados.
- **Cinzel** (rótulos em versalete), que conversa com as inscrições dos logos.
- **Figtree** (corpo), legível e calma.

## Movimento
- Entradas com fade e subida leve (IntersectionObserver), com atrasos escalonados que são zerados depois.
- Hero: raios que se desenham, lema que sobe linha a linha, foto que se abre "como portas".
- Um elemento vivo por seção escura: luz que respira no Carisma, halo no ícone, chama que tremula.
- Camada de ambiente fixa: brilho quente em deriva lenta (90 s) com grão.
- **Momento interativo:** "Acenda uma vela": segurar o botão acende a vela e leva ao pedido de oração. Soltar antes volta devagar. Com "reduzir movimento", a vela já aparece acesa.
- `prefers-reduced-motion` respeitado, inclusive se mudar com a página aberta. Aba escondida pausa as animações.

## Mapa e chamadas
Duas chamadas principais lado a lado: **Vocação** (marrom) e **Apoie** (carmim). Pedido de oração como terceira porta, pela vela.

## Textos para a Fraternidade validar
- Descrição dos símbolos (página História): interpretação a partir das imagens, sem texto oficial no site antigo.
- Etapas da formação (página Vocação): baseadas nos cargos de mestre citados no site antigo.
- Horários de missa, valor de R$ 25, contas bancárias e e-mails: dados de 2017 a 2020.
- Governo geral 2026-2031: bloco "em breve" até recebermos os nomes.
