# Design System — Imersão Empresa Independente

> **Página de referência:** https://lps.empresaindependente.com.br/ev
> **Campanha:** Imersão Empresa Independente — evento presencial, 25 e 26 de julho, Florianópolis (Ingleses / Costão Golf)
> **Stack da página:** HTML estático + Tailwind via CDN (`cdn.tailwindcss.com`) com `tailwind.config` inline. Sem build. Toda a estilização vive no próprio HTML.
> **Tokens CSS reutilizáveis:** `design-tokens-imersao-ev.css` (mesma pasta)

> ⚠️ **Não confundir** com o projeto imobiliário "Évora Charm Village" (`Evora/`, `evora-charm-village.html`). São campanhas totalmente distintas; este DS cobre **apenas** o evento "Imersão".

---

## 1. Visão geral e princípios de design

A landing é uma **página de vendas dark, premium e de alta urgência controlada** para um evento B2B de empresários. O sistema visual apoia quatro objetivos de conversão:

| Princípio | Como se manifesta |
|-----------|-------------------|
| **Dark premium** | Fundo quase-preto (`#0a0806`), superfícies em camadas (`#0a0a0a` → `#121212`), bordas brancas de baixa opacidade (5–20%) em vez de linhas duras. Acabamento sofisticado, sem ruído. |
| **Accent único e disciplinado** | Um só sistema de cor de marca: teal/verde-água (`#02b9a9` + variações). Usado com parcimônia para guiar o olho a urgência e CTAs. Nada compete com ele. |
| **Urgência controlada (não "falsa")** | A escassez ("Lote 3", "menos de 30 ingressos", "40% OFF") é repetida em pills pulsantes e barra de countdown — mas a copy explicitamente se distancia de urgência falsa. Visual de urgência é sóbrio, não estridente. |
| **Prova social pesada** | Órbita/marquee de fotos de palestrantes, marquee de "presenças confirmadas" com avatares, logos de patrocinadores, faixa de palavras-chave. Movimento constante = ambiente lotado e vivo. |
| **Contraste de foco: escuro → claro** | Corpo da página é escuro; seções de conversão/confiança (FAQ, CTA final, footer) invertem para **fundo branco**, criando um "respiro" e destacando o fechamento. |

**Tom:** confiante, direto, "sala fechada com as pessoas certas". Headlines curtas e afiadas. Números grandes (preço, horários) em fonte display para impacto.

---

## 2. Design tokens

### 2.1 Cores

#### Superfícies / fundos
| Token | Hex | Uso |
|-------|-----|-----|
| `body` | `#0a0806` | Fundo global do `<body>` |
| `dark` | `#0a0a0a` | Fundo de seção padrão (`bg-dark`) |
| `darker` | `#090909` | Fundo mais profundo / base de gradientes |
| `card` | `#121212` | Fundo de card; cápsula circular do ícone em CTA |
| hero-top | `#171717` | Topo do gradiente do hero |
| surface-light | `#ffffff` | Seções invertidas: FAQ, CTA final, footer |

#### Marca / accent (teal — verde-água)
| Token | Hex | Uso |
|-------|-----|-----|
| `accent` | `#02b9a9` | **Cor de marca.** CTA secundário sólido, dots pulsantes, selos "40% OFF", bordas de destaque |
| `accent-light` | `#6edcd2` | Texto de destaque sobre escuro, estados hover, fim claro de gradientes |
| `accent-dark` | `#074b45` | Bordas de gradiente, base de sombras/glows |
| accent-glow | `#18f1de` | Ciano vibrante do **inset glow** em cards premium |
| accent-bright | `#b8fff9` | Ciano quase-branco no topo do glow radial do CTA final |
| accent-mid | `#0c7b71` | Base do gradiente linear dos cards premium |
| accent-deepest | `#001917` | Fim do glow radial |

#### Texto
| Token | Hex | Uso |
|-------|-----|-----|
| text | `#f5f5f5` | Texto padrão sobre escuro |
| text-strong | `#f7f7f7` | Títulos/ênfase sobre escuro |
| text-on-light | `#141414` | Texto sobre fundo branco |
| text-cta-dark | `#1f2937` (gray-800) | Texto do CTA de fundo branco |

Opacidades de texto recorrentes sobre escuro: `text-white/90` (ênfase), `/70` e `/60` (corpo), `/50` e `/40` (microcopy/legenda), `/30` (rótulos apagados).

#### Semânticas — comparativo "lado certo vs errado"
| Token | Hex | Uso |
|-------|-----|-----|
| positive | `#02b9a9` (accent) | Check ✓ — "onde o negócio funciona para você" |
| negative | `#ff5f56` | Fundo do ícone ✕ a **15% de opacidade** (`bg-[#ff5f56]/15`) |
| negative-stroke | `#ff8a8a` | Traço do ícone ✕ |

#### Utilitárias
| Token | Hex | Uso |
|-------|-----|-----|
| faq-icon-bg | `#c4c4c4` | Fundo do "+" no accordion FAQ |
| faq-icon-stroke | `#191d24` | Traço do "+" no accordion FAQ |
| whatsapp | `#25D366` | FAB flutuante do WhatsApp |
| sticky-mobile | `#141414` @ 85% | Barra sticky de CTA no rodapé mobile (+ backdrop-blur) |

#### Gradientes
| Nome | Valor | Uso |
|------|-------|-----|
| `gradient-text` | `linear-gradient(135deg, #6edcd2, #02b9a9)` | Texto com clip (`.gradient-text`) |
| gradient-countdown | `linear-gradient(90deg, #074b45, #02b9a9 50%, #074b45)` | Barra de countdown fixa |
| gradient-keywords | `linear-gradient(270deg, #6edcd2, #02b9a9 49%, #074b45)` | Faixa horizontal de palavras-chave |
| gradient-hero | `linear-gradient(#171717, #090909)` | Fundo do hero |
| gradient-card-premium | `linear-gradient(#000, #0c7b71)` | Fundo dos cards premium (Experience, comparativo positivo) |
| gradient-cta-glow | `radial-gradient(100% 180% at 89.2% 10.7%, #b8fff9, #6edcd2 24%, #02b9a9 52%, #074b45 77%, #001917)` | Card de CTA final |
| image-overlay | `linear-gradient(to top, black/80, transparent)` | Overlay sobre fotos (cards de palestrante, dias) |

### 2.2 Tipografia

**Famílias** (via `@font-face` woff2 self-hosted em `framerusercontent.com`):
- **`Neue Montreal`** (sans) — corpo, UI, títulos. Pesos: 400 / 500 / 700. Fallback: `Inter, system-ui, sans-serif`.
- **`Thunder`** (display) — números gigantes de horário e rótulos de impacto. Peso único: **600**. Fallback: `Neue Montreal`.

**Escala** (com contexto de uso):
| Classe Tailwind | Tamanho | Uso |
|-----------------|---------|-----|
| `text-xs` | 12px | Legendas, selos "40% OFF", microcopy de escassez |
| `text-sm` | 14px | Corpo de UI, labels, itens de lista, badges |
| `text-base` | 16px | Parágrafos secundários |
| `text-lg` | 18px | Subtítulos, corpo de destaque |
| `text-xl` | 20px | Títulos de card (comparativo) |
| `text-2xl` | 24px | H2 de seção no mobile |
| `text-3xl` | 30px | H1 hero mobile |
| `text-[28px]` | 28px | Nomes de palestrante, títulos de blocos de dia/cronograma |
| `text-[40px]` | 40px | H2 de seção no desktop (`md:`) |
| `text-5xl` | 48px | H1 hero desktop (`md:`) |
| `text-5xl/6xl` | 48–60px | Preço grande dos ingressos |
| `text-[160px]` | 160px | Rótulo fantasma "PRIMEIRO/SEGUNDO DIA" (`white/10`) |
| `text-[200px]` | 200px | **Número de horário gigante** (Thunder) na timeline desktop |

**Padrões de tratamento:**
- `tracking-tight` no H1 do hero.
- `tracking-[0.15em]` em eyebrows/pills uppercase de urgência.
- `tracking-[0.3em]` na faixa de palavras-chave.
- `tracking-[0.35em]` no eyebrow "Presenças Confirmadas".
- `leading-[1.2]` em headlines; `leading-[1.5]`–`[1.7]` em corpo.
- Headlines de seção geralmente `font-normal` ou `font-medium` (não bold) — elegância sobre peso.

### 2.3 Espaçamento
- **Vertical de seção:** `py-16` (mobile) → `md:py-24` (blocos de urgência/garantia) ou `md:py-36` (seções de conteúdo amplas).
- **Horizontal:** `px-6` (mobile) → `md:px-16` (desktop). Hero usa `px-5 md:px-16`.
- **Container central:** `max-w-[1216px] mx-auto`. Blocos de texto centrados usam larguras menores (`max-w-[663px]`, `[720px]`, `[860px]`).
- **Gap entre cards:** `gap-2` (grids justas de cards premium/preços) a `gap-4`/`gap-8` (grids de palestrante e conteúdo).

### 2.4 Border-radius
| Classe | Uso |
|--------|-----|
| `rounded-lg` | Inputs, badges/labels pequenos, thumbnails de programação |
| `rounded-xl` | Cards de conteúdo (comparativo, value-framing, ingressos) |
| `rounded-2xl` | Cards grandes (palestrantes, wrapper do bloco de preços, itens de FAQ) |
| `rounded-3xl` | Card de CTA final |
| `rounded-full` | Pills, botões, avatares, dots, cápsulas de ícone, FAB |

### 2.5 Sombras / glows
- **Card premium** (Experience + comparativo positivo):
  `box-shadow: 0 4.5px 100px rgba(1,185,168,0.1), inset 0 -28px 59px -18px #18f1de, inset 0 44px 37px -54px rgba(23,241,221,0.6);`
  Combinar sempre com `background: linear-gradient(#000, #0c7b71)`.
- **CTA final glow** (externo, multicamada):
  `box-shadow: 0 18px 39px rgba(3,73,68,0.21), 0 71px 71px rgba(3,73,68,0.18), 0 159px 95px rgba(3,73,68,0.11);`
- **Avatares confirmados:** `ring-1 ring-white/10 shadow-lg`.

### 2.6 Bordas sutis
`border-white/5` (separação discreta) · `border-white/10` (card padrão) · `border-white/20` (card destacado / badge no hero) · `border-[#02b9a9]/40` (pill de urgência). Sobre fundo branco: `border-dark/10`.

### 2.7 Breakpoints (Tailwind default)
`sm 640px` · `md 768px` · `lg 1024px` · `xl 1280px`. Cortes principais: **`md`** (mobile↔desktop de layout e tipografia) e **`lg`** (timelines e grids de 3 colunas). Vários componentes têm **variante mobile e desktop separadas no HTML** (`lg:hidden` / `hidden lg:flex`) — ver §3.

### 2.8 Layout fixo / z-index
`body { padding-top: 40px }` reserva a barra de countdown (`z-100`). Sticky CTA mobile `z-50`. WhatsApp FAB `z-40`. Mobile reserva `padding-bottom: 80px` para o sticky bar.

---

## 3. Biblioteca de componentes

Cada componente traz propósito, classes-chave e um trecho reutilizável.

### 3.1 Barra de countdown (fixa, topo)
**Propósito:** urgência persistente + CTA sempre visível. Fixa no topo; `body` compensa com `padding-top: 40px`.
```html
<div class="fixed top-0 left-0 right-0 z-[100] flex items-center justify-center gap-3 px-4 py-2 text-sm font-medium"
     style="background: linear-gradient(90deg, #074b45, #02b9a9 50%, #074b45);">
  <span class="text-white">40% OFF com menos de 30 ingressos disponíveis</span>
  <a href="#" class="hidden sm:flex items-center gap-1 bg-white text-[#074b45] text-xs px-3 py-1 rounded-full hover:bg-gray-100 transition ml-1">
    <span>Garantir agora</span>
    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg>
  </a>
</div>
```

### 3.2 Badge / pill informativo
**Propósito:** metadados do evento (data, local) e etiquetas de seção.
- **Neutro (hero):** `px-3 py-2 rounded-lg border-t border-white/20 bg-white/5 backdrop-blur-sm` + ícone SVG stroke `white/50`.
- **Etiqueta de seção:** `text-sm font-medium text-white px-3 py-2 rounded-lg border border-white/10`.
```html
<div class="flex items-center gap-2 px-3 py-2 rounded-lg border-t border-white/20 bg-white/5 backdrop-blur-sm">
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><!-- ícone calendário/pin --></svg>
  <span class="text-sm font-medium">25 e 26 de julho</span>
</div>
```

### 3.3 Pill de urgência (com dot pulsante)
**Propósito:** sinalizar escassez/"ao vivo". Sempre com `animate-pulse` no dot e texto em `accent-light` uppercase.
```html
<div class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-[#02b9a9]/40 bg-[#02b9a9]/10">
  <span class="w-2 h-2 rounded-full bg-[#02b9a9] animate-pulse"></span>
  <span class="text-sm font-medium text-[#6edcd2] uppercase tracking-[0.15em]">Lote 3 · 40% OFF · menos de 30 ingressos disponíveis</span>
</div>
```

### 3.4 Botão CTA — padrão "texto + cápsula com seta ↗"
**Propósito:** padrão de CTA universal da página. Pill com cápsula circular à direita contendo a seta diagonal.

**Três variantes:**
| Variante | Classes do pill | Cápsula |
|----------|-----------------|---------|
| **Primário branco** (default) | `bg-white text-gray-800 pl-4 pr-1 py-1 rounded-full hover:bg-gray-100` | `bg-[#121212]` (ícone branco) |
| **Accent sólido** (urgência) | `bg-[#02b9a9] text-white pl-5 pr-2 py-2 rounded-full hover:bg-[#6edcd2] hover:text-dark` | `bg-white/20` |
| **Fantasma / outline** | `text-white border border-white/20 pl-4 pr-1 py-1 rounded-full hover:bg-white/5` | `bg-white/10` |
```html
<a href="#" class="flex items-center gap-1 bg-white text-gray-800 text-sm pl-4 pr-1 py-1 rounded-full hover:bg-gray-100 transition">
  <span>Garantir meu lugar com 40% OFF</span>
  <span class="w-8 h-8 rounded-full bg-[#121212] flex items-center justify-center shrink-0">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg>
  </span>
</a>
```
**Ícone seta diagonal (reutilizável):** `<path d="M7 17L17 7"/><path d="M7 7h10v10"/>` em viewBox `0 0 24 24`.

### 3.5 Card de palestrante
**Propósito:** grade de autoridade. Imagem full-bleed + overlay + nome/cargo ancorados no rodapé. Altura fixa 600px.
```html
<div class="relative rounded-2xl overflow-hidden bg-card h-[600px] border border-white/20 group">
  <img src="..." alt="Nome" class="absolute inset-0 w-full h-full object-cover object-top transition-all duration-500">
  <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
  <div class="absolute bottom-12 left-12 z-10">
    <h3 class="text-[28px] leading-[1.2] text-white">Gabriel Breier</h3>
    <p class="text-sm font-medium text-[#f7f7f7] mt-1">CEO EMPRESA INDEPENDENTE</p>
  </div>
</div>
```
Grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`.

### 3.6 Marquee / ticker infinito
**Propósito:** movimento contínuo = prova social/energia. Track duplicado (set A + set B `aria-hidden`) deslizando `translateX(-50%)`; pausa no hover; fade nas bordas via máscara.
```css
@keyframes marquee-confirmados { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.marquee-confirmados { animation: marquee-confirmados 45s linear infinite; width: max-content; display: flex; }
.marquee-confirmados:hover { animation-play-state: paused; }
.confirmados-fade {
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
          mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
}
```
**Variações na página:** fotos de palestrante no hero mobile (`ticker-photos`, 25s), presenças confirmadas com avatares (45s), faixa de palavras-chave (`ticker-keywords`, 20s). Avatar confirmado: `w-24 h-24 rounded-full ring-1 ring-white/10 shadow-lg` + legenda `text-sm text-white/70`.

### 3.7 Faixa de palavras-chave (keyword ticker)
**Propósito:** reforço de temas em faixa gradiente teal entre seções.
```html
<div class="h-20 overflow-hidden flex items-center" style="background: linear-gradient(270deg, #6edcd2, #02b9a9 49%, #074b45);">
  <div class="flex items-center gap-10 ticker-keywords whitespace-nowrap">
    <span class="text-sm font-medium text-white uppercase tracking-[0.3em]">vendas</span>
    <span class="text-sm font-medium text-white/30 tracking-[0.3em]">///</span>
    <!-- repetir termos; duplicar conjunto para loop contínuo -->
  </div>
</div>
```

### 3.8 Card comparativo (lado certo ✓ vs lado errado ✕)
**Propósito:** contrastar dois cenários. Card positivo usa gradiente premium + glow; card neutro usa borda simples.
- **Item positivo:** cápsula `bg-white/10` + check `M14 7L8.5 12.5L6 10` (stroke branco).
- **Item negativo:** cápsula `bg-[#ff5f56]/15` + X `M6 6L14 14M14 6L6 14` (stroke `#ff8a8a`).
```html
<!-- Card positivo -->
<div class="rounded-xl p-2 overflow-hidden"
     style="background: linear-gradient(#000, #0c7b71); box-shadow: 0 4.5px 100px rgba(1,185,168,0.1), inset 0 -28px 59px -18px #18f1de, inset 0 44px 37px -54px rgba(23,241,221,0.6);">
  <div class="rounded aspect-video overflow-hidden mb-8"><img src="..." class="w-full h-full object-fill"></div>
  <div class="p-8 pt-0">
    <h4 class="text-xl font-medium text-[#f7f7f7] mb-4">Onde o negócio funciona para você</h4>
    <div class="flex items-center gap-3 py-3 border-b border-white/10">
      <div class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0">
        <svg width="12" height="12" viewBox="0 0 20 20" fill="none"><path d="M14 7L8.5 12.5L6 10" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
      </div>
      <span class="text-sm text-white opacity-70">Time executa sem precisar te consultar</span>
    </div>
    <!-- demais itens -->
  </div>
</div>
```

### 3.9 Card de ingresso / preço (Experience vs Pass)
**Propósito:** oferta. Wrapper `rounded-2xl border border-white/10 backdrop-blur-[42px]` envolve dois cards `grid lg:grid-cols-2`. Card destacado (Experience) usa gradiente premium + glow; card padrão (Pass) usa borda. Selo "40% OFF" no canto superior direito. Lista de benefícios (mesmo padrão de check do §3.8). Bloco de preço central.
```html
<div class="relative rounded-xl p-2 overflow-hidden"
     style="background: linear-gradient(#000, #0c7b71); box-shadow: 0 4.5px 100px rgba(1,185,168,0.1), inset 0 -28px 59px -18px #18f1de, inset 0 44px 37px -54px rgba(23,241,221,0.6);">
  <span class="absolute top-4 right-4 z-10 bg-[#02b9a9] text-white text-[11px] font-semibold uppercase tracking-wide px-3 py-1 rounded-full shadow-lg">40% OFF</span>
  <div class="rounded aspect-video overflow-hidden"><img src="..." class="w-full h-full object-cover"></div>
  <div class="p-8">
    <h3 class="text-[28px] leading-[1.2] text-[#f7f7f7] text-center mb-4">Experience</h3>
    <!-- lista de benefícios com check -->
    <div class="text-center mb-6">
      <span class="inline-block text-sm font-medium text-white px-3 py-2 rounded-lg border border-white/10 mb-2">Ingresso Experience (Lote 3)</span>
      <p class="text-white/50 text-lg">R$ 1.197,00 ou 12x de</p>
      <p class="text-white text-5xl md:text-6xl font-normal mt-1">R$ 120,18</p>
      <p class="text-xs text-[#6edcd2] mt-3 leading-[1.4]">40% OFF por tempo limitado. Menos de 30 ingressos disponíveis.</p>
    </div>
    <!-- CTA primário branco full-width -->
  </div>
</div>
```
**Preços de referência (Lote 3):** Experience R$ 1.197,00 (12x R$ 120,18) · Pass R$ 347,00 (12x R$ 34,84). Cupom `40%off` é anexado via JS aos links de checkout Monetizze.

### 3.10 Timeline de programação (números de horário gigantes)
**Propósito:** cronograma por dia. Desktop: número gigante Thunder (`text-[200px]`) + thumb + texto em linha. Mobile: card com foto de fundo e horário inline. Rótulo fantasma do dia em `text-[160px] text-white/10`.
```html
<!-- rótulo fantasma -->
<p class="text-[40px] md:text-[100px] lg:text-[160px] font-medium text-white/10 text-center leading-none mb-8">PRIMEIRO DIA</p>
<!-- item desktop -->
<div class="flex flex-row items-center gap-16 reveal">
  <p class="text-[200px] font-semibold text-white uppercase leading-none w-[220px] flex-shrink-0 text-right" style="font-family: Thunder;">9h</p>
  <div class="rounded-lg overflow-hidden w-[40%] h-[250px]"><img src="..." class="w-full h-full object-cover"></div>
  <div class="flex-1">
    <h3 class="text-[28px] leading-[1.2] text-white mb-3">Credenciamento</h3>
    <p class="text-lg text-[#f5f5f5] opacity-70 leading-[1.5]">Chegue cedo, retire seu kit exclusivo...</p>
  </div>
</div>
```

### 3.11 Bloco de garantia
**Propósito:** reduzir risco. Ícone escudo em círculo accent + headline + microcopy.
```html
<div class="max-w-[720px] mx-auto flex flex-col items-center gap-6 text-center reveal">
  <div class="w-14 h-14 rounded-full border border-[#02b9a9]/40 bg-[#02b9a9]/10 flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6edcd2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
  </div>
  <h2 class="text-2xl md:text-[32px] leading-[1.3] font-normal text-white">Se você participar do primeiro dia inteiro e sentir que não valeu, devolvemos 100%.</h2>
  <p class="text-lg text-white/50">Sem burocracia, sem perguntas. O risco é todo nosso.</p>
</div>
```

### 3.12 Accordion de FAQ (seção invertida branca)
**Propósito:** objeções. Fundo **branco**. Ícone "+" cinza que rotaciona 45° (vira "×") ao abrir; resposta expande via `max-height`.
```html
<div class="faq-item border border-dark/10 rounded-2xl bg-white overflow-hidden cursor-pointer p-4" onclick="this.classList.toggle('open')">
  <div class="flex items-center justify-between">
    <p class="text-lg text-dark font-medium">O que é a Imersão Empresa Independente</p>
    <div class="w-[38px] h-[38px] rounded-full bg-[#c4c4c4] flex items-center justify-center faq-icon">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <line x1="7" y1="3" x2="7" y2="11" stroke="#191d24" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="3" y1="7" x2="11" y2="7" stroke="#191d24" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </div>
  </div>
  <div class="faq-answer"><p class="text-dark/70 mt-4 text-base leading-[1.5]">Resposta...</p></div>
</div>
```
```css
.faq-answer { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
.faq-item.open .faq-answer { max-height: 200px; }
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-icon { transition: transform 0.3s ease; }
```

### 3.13 Card de CTA final (glow radial)
**Propósito:** fechamento de alta conversão. Card `rounded-3xl` com glow radial teal e sombra multicamada. Fica em seção de fundo branco (`hidden md:block` — no mobile o fechamento é o sticky bar).
```html
<div class="rounded-3xl p-8 flex flex-col items-center justify-center gap-8 min-h-[546px] relative overflow-hidden"
     style="background: radial-gradient(100% 180% at 89.2% 10.7%, #b8fff9, #6edcd2 24%, #02b9a9 52%, #074b45 77%, #001917); box-shadow: 0 18px 39px rgba(3,73,68,0.21), 0 71px 71px rgba(3,73,68,0.18), 0 159px 95px rgba(3,73,68,0.11);">
  <div class="text-center max-w-[500px] z-10">
    <h2 class="text-2xl md:text-[40px] leading-[1.2] font-normal text-white mb-4">Último lote. 40% OFF. Menos de 30 ingressos.</h2>
    <p class="text-lg text-white opacity-70 leading-[1.5] max-w-[399px] mx-auto mb-8">...</p>
    <!-- CTA primário branco -->
  </div>
</div>
```

### 3.14 Sticky CTA mobile + FAB WhatsApp
**Propósito:** conversão persistente no mobile.
```html
<!-- Sticky bar (mobile) -->
<div class="md:hidden fixed bottom-0 left-0 right-0 z-50 px-4 py-3 bg-[#141414]/85 backdrop-blur-xl border-t border-white/10">
  <a href="#" class="flex items-center justify-center gap-1 bg-white text-gray-800 text-sm font-medium pl-4 pr-1 py-1.5 rounded-full hover:bg-gray-100 transition w-full">
    <span>Garantir meu lugar com 40% OFF</span>
    <span class="w-8 h-8 rounded-full bg-[#121212] flex items-center justify-center shrink-0"><!-- seta ↗ --></span>
  </a>
</div>
<!-- WhatsApp FAB -->
<a href="https://wa.me/55...?text=..." class="fixed bottom-24 md:bottom-6 right-4 md:right-6 z-40 w-14 h-14 rounded-full bg-[#25D366] flex items-center justify-center shadow-lg hover:scale-105 transition">
  <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><!-- glifo WhatsApp --></svg>
</a>
```

### 3.15 Faixa de logos de patrocinadores
**Propósito:** autoridade. Faixa curta, logos monocromáticos a `opacity-25`.
```html
<div class="bg-dark h-[104px] rounded-[10px] flex items-center justify-center gap-3 sm:gap-8 md:gap-16 px-3 md:px-6 overflow-hidden">
  <img src="..." alt="Fullstack" class="h-5 sm:h-8 md:h-10 opacity-25 max-w-full">
  <!-- demais logos -->
</div>
```

---

## 4. Padrões de animação / interação

| Padrão | Definição | Onde usar |
|--------|-----------|-----------|
| **Reveal on scroll** | `.reveal { opacity:0; transform:translateY(40px); transition:opacity .8s ease, transform .8s ease; }` + `.visible` via `IntersectionObserver` (threshold 0.1). | Aplicar `class="reveal"` em todo bloco de conteúdo que entra na viewport. |
| **Marquee** | `translateX(0 → -50%)` linear infinito; track duplicado; `animation-play-state: paused` no hover. | Fotos hero mobile (25s), confirmados (45s), keywords (20s). |
| **Órbita do hero** | Anel de imagens girando (`spin-slow` 60s) com contra-rotação (`counter-spin` 60s) nas thumbs para mantê-las na vertical. Desktop apenas. | Fundo do hero. |
| **Pulse** | `animate-pulse` no dot dos pills de urgência. | Todo indicador de escassez/"ao vivo". |
| **Accordion** | `max-height` 0 → 200px + ícone rotate 45° (`.open`), `transition .3s ease`. | FAQ. |
| **Hover states** | CTA branco → `hover:bg-gray-100`; CTA accent → `hover:bg-[#6edcd2] hover:text-dark`; FAB → `hover:scale-105`; imagens de card → `transition-all duration-500`. | CTAs, cards, FAB. |
| **Navbar hide/show** | Ao rolar para baixo (>200px) esconde (`translateY(-120px)`), ao subir revela. `transition .3s ease`. | Navegação (quando presente). |
| **Smooth scroll** | `html { scroll-behavior: smooth; }` para âncoras (`#ingressos`, `#faq`...). | Navegação interna. |

---

## 5. Diretrizes de uso

### 5.1 Quando usar cada estilo de CTA
- **Primário branco (cápsula `#121212`)** — CTA padrão e de maior frequência. Use como ação principal em fundos escuros e dentro dos cards de preço/CTA final. É o "botão default".
- **Accent sólido (`#02b9a9`, cápsula `white/20`)** — reserve para **blocos de urgência dedicados** (seção de escassez, promoção relâmpago). Sinaliza "aja agora".
- **Fantasma / outline (`border-white/20`)** — CTA **secundário** ao lado de um primário (ex.: no hero, "2 dias + Costão Golf" é secundário ao "Garantir meu lugar"). Nunca isolado.
- Todo CTA mantém o padrão **texto + cápsula circular com seta ↗**. Não invente novos formatos.

### 5.2 Hierarquia de urgência (do mais leve ao mais forte)
1. **Badge neutro** (data/local) — informativo, sem cor de marca.
2. **Etiqueta de seção** (`border-white/10`) — organizacional.
3. **Pill de urgência accent com dot pulsante** — escassez ("Lote 3", "menos de 30 ingressos").
4. **Barra de countdown fixa** + **seções dedicadas de escassez** (fundo `#0a0a0a`, borda `border-y border-white/5`) — pressão máxima.

Mantenha a mensagem de escassez **consistente**: "40% OFF", "Lote 3 / último lote", "menos de 30 ingressos", "sem reabertura". Repita o mesmo texto; não crie números concorrentes.

### 5.3 Aplicando em novas seções/páginas da campanha
- **Importe** `design-tokens-imersao-ev.css` e mantenha `tailwind.config` com as cores `dark/darker/card/accent/accent-light/accent-dark` e as famílias `sans`/`display`.
- **Ritmo de seção:** `py-16 md:py-36` para conteúdo, `py-16 md:py-24` para blocos curtos (urgência/garantia); container `max-w-[1216px] mx-auto`; padding `px-6 md:px-16`.
- **Estrutura padrão de seção:** eyebrow/etiqueta → H2 (`text-2xl md:text-[40px] font-normal`) → corpo (`text-lg text-white/70`) → CTA. Envolva com `class="reveal"`.
- **Inversão de contraste:** use fundo **branco** apenas para seções de confiança/fechamento (FAQ, CTA final, footer). O restante permanece escuro.
- **Accent com disciplina:** verde-água só para urgência, CTAs, checks e destaques pontuais. Nunca em grandes áreas de texto corrido.
- **Prova social sempre em movimento:** prefira marquees/tickers a grids estáticos quando o objetivo é "ambiente cheio".
- **Números de impacto** (preços, horários) em `Thunder` grande; texto corrido sempre em `Neue Montreal`.
- **Cards premium** (destaque/oferta) = `linear-gradient(#000,#0c7b71)` + o `box-shadow` de glow. Cards secundários = borda `border-white/10`. Nunca aplique o glow a mais de um card por par (destaque único).

### 5.4 Referência de estrutura de página (top → bottom)
countdown bar → hero (badges + H1 + subtítulo + 2 CTAs + órbita/marquee de fotos) → logos patrocinadores → urgência do lote → palestrantes (grid) → presenças confirmadas (marquee) → faixa de palavras-chave → comparativo dois tipos de empresário → programação dia 1/dia 2 (imagens) → cronograma (timeline com horários gigantes) → promoção relâmpago → ingressos (value-framing + Experience/Pass) → garantia → FAQ (branco) → CTA final (branco, glow) → footer (branco) → sticky CTA mobile + FAB WhatsApp.
