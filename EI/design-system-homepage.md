# Design System — Homepage (ai.empresaind.com)

> Documentação visual e técnica do layout da homepage da Empresa Independente.
> Escopo: apenas o site marketing (homepage), não o sistema/dashboard.

---

## 1. Identidade Visual

### Direção Estética
**Dark-first, tech-premium, cyan glow.** A homepage usa exclusivamente tema escuro (`className="dark"` no layout), transmitindo sofisticação e modernidade. O contraste alto entre fundo escuro e acentos cyan/emerald cria uma identidade visual memorável.

### Logo
- **Marca:** "EI" (sigla) + "Empresa Independente" (texto)
- **Formato header:** Ícone quadrado arredondado `bg-primary` com "EI" em bold + texto ao lado
- **Tamanho ícone:** `h-8 w-8` (32px), texto `font-bold text-lg`

---

## 2. Paleta de Cores

### Cores Primárias (Dark Mode — único tema do site)

| Token | Valor OKLCh | Hex Aprox. | Uso |
|-------|-------------|------------|-----|
| `--background` | `oklch(0.145 0 0)` | `#1a1a1a` | Fundo principal |
| `--foreground` | `oklch(0.985 0 0)` | `#fafafa` | Texto principal |
| `--primary` | `oklch(0.765 0.177 163.223)` | `#34d399` | CTAs, links, acentos |
| `--primary-foreground` | `oklch(0.145 0.05 170)` | `#0a2e24` | Texto sobre primary |
| `--muted` | `oklch(0.269 0 0)` | `#333333` | Backgrounds sutis |
| `--muted-foreground` | `oklch(0.708 0 0)` | `#a3a3a3` | Texto secundário |
| `--card` | `oklch(0.205 0 0)` | `#262626` | Fundo de cards |
| `--border` | `oklch(1 0 0 / 10%)` | `rgba(255,255,255,0.1)` | Bordas |
| `--destructive` | `oklch(0.704 0.191 22.216)` | `#ef4444` | Erros, "X" na comparação |

### Cores por Parte do Framework

Cada parte tem cor única usada em gradientes de card e ícones:

| Parte | Cor | Gradient (card bg) | Ícone |
|-------|-----|-------------------|-------|
| 1 — Matriz Tempo | Emerald | `from-emerald-500/20 to-emerald-600/5` | `text-emerald-400` |
| 2 — Delegação | Violet | `from-violet-500/20 to-violet-600/5` | `text-violet-400` |
| 3 — Contratação | Amber | `from-amber-500/20 to-amber-600/5` | `text-amber-400` |
| 4 — Estruturação | Blue | `from-blue-500/20 to-blue-600/5` | `text-blue-400` |
| 5 — Processos | Rose | `from-rose-500/20 to-rose-600/5` | `text-rose-400` |
| 6 — Ritos | Cyan | `from-cyan-500/20 to-cyan-600/5` | `text-cyan-400` |
| 7 — Projetos | Orange | `from-orange-500/20 to-orange-600/5` | `text-orange-400` |
| 8 — Pessoas | Pink | `from-pink-500/20 to-pink-600/5` | `text-pink-400` |
| 9 — Líderes | Yellow | `from-yellow-500/20 to-yellow-600/5` | `text-yellow-400` |

### Efeitos de Glow

```css
/* CTA buttons e cards premium */
.glow-emerald {
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.15), 0 0 60px rgba(16, 185, 129, 0.05);
}
.glow-emerald-strong {
  box-shadow: 0 0 30px rgba(16, 185, 129, 0.25), 0 0 80px rgba(16, 185, 129, 0.1);
}
```

### Gradientes Recorrentes

| Nome | Código | Uso |
|------|--------|-----|
| Hero glow | `bg-primary/20 blur-3xl rounded-full` | Background glow atrás do hero |
| Section divider | `bg-gradient-to-b from-background via-primary/5 to-background` | Transição entre seções |
| Text gradient | `bg-gradient-to-r from-primary via-emerald-400 to-primary bg-clip-text text-transparent` | "sem você?" no headline |
| CTA gradient border | `bg-gradient-to-r from-primary/20 via-primary/40 to-primary/20` | Borda do diagnostic CTA |

---

## 3. Tipografia

### Font Family
- **Sans-serif:** `var(--font-geist-sans)` — Geist Sans (Next.js default)
- **Monospace:** `var(--font-geist-mono)` — Geist Mono

### Hierarquia Tipográfica

| Elemento | Mobile | Desktop | Weight | Uso |
|----------|--------|---------|--------|-----|
| H1 (Hero) | `text-4xl` (36px) | `text-6xl` → `text-7xl` | `font-bold` | Headline principal |
| H2 (Section) | `text-3xl` (30px) | `text-4xl` → `text-5xl` | `font-bold` | Títulos de seção |
| H3 (Card title) | `text-lg` (18px) | `text-xl` (20px) | `font-semibold` | Títulos de cards |
| Body | `text-base` (16px) | `text-lg` (18px) | `font-normal` | Parágrafos |
| Small | `text-sm` (14px) | `text-sm` | `font-normal` | Descrições secundárias |
| Caption | `text-xs` (12px) | `text-xs` | `font-medium` | Badges, labels |
| Stat number | `text-3xl` (30px) | `text-3xl` | `font-bold` | Números de destaque |

### Cores de Texto

| Tipo | Classe | Uso |
|------|--------|-----|
| Principal | `text-foreground` | Headlines, corpo principal |
| Secundário | `text-muted-foreground` | Descrições, subtítulos |
| Acento | `text-primary` | Links, CTAs, destaques |
| Destaque em quote | `text-primary font-semibold` | Métricas em depoimentos |

---

## 4. Espaçamento

### Seções
- **Padding vertical:** `py-20 md:py-28` (80px → 112px)
- **Padding horizontal:** `px-4` (16px) — container interno faz o resto

### Containers
| Tipo | Classe | Largura Max |
|------|--------|------------|
| Narrow | `max-w-4xl mx-auto` | 896px |
| Default | `max-w-5xl mx-auto` | 1024px |
| Wide | `max-w-6xl mx-auto` | 1152px |

### Grid Gaps
| Contexto | Gap |
|----------|-----|
| Cards grid | `gap-4` (16px) mobile → `gap-6` (24px) desktop |
| Section header → content | `mb-12` → `mb-16` (48-64px) |
| Stacked elements | `space-y-3` → `space-y-6` |

### Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-sm` | 6px | Badges, inputs pequenos |
| `--radius-md` | 8px | Botões |
| `--radius-lg` | 10px | Cards |
| `--radius-xl` | 14px | Cards maiores |
| `rounded-full` | 9999px | Badges pill, avatares |

---

## 5. Componentes

### 5.1 Header (Sticky)

```
┌─────────────────────────────────────────────────────────┐
│ [EI] Empresa Independente   Método Comparação Preços Blog Sobre   [Entrar] [Começar grátis] │
└─────────────────────────────────────────────────────────┘
```

- **Posição:** `sticky top-0 z-50`
- **Background:** `bg-background/80 backdrop-blur-md`
- **Borda inferior:** `border-b border-border`
- **Altura:** implícita via `py-3 px-4`
- **Nav links:** `text-sm text-muted-foreground hover:text-primary transition-colors`
- **Botão "Entrar":** `variant="ghost" size="sm"`
- **Botão "Começar grátis":** `variant="default" size="sm"` (bg-primary)
- **Mobile:** Nav oculta, hambúrguer menu (sheet dropdown)

### 5.2 Hero Section

```
┌─────────────────────────────────────────┐
│          [glow circle bg-primary/20]     │
│                                          │
│   ┌─ badge ──────────────────────┐       │
│   │ 🤖 Framework + IA para gestão │       │
│   └──────────────────────────────┘       │
│                                          │
│   Sua empresa funciona                   │
│   sem você?          ← gradient text     │
│                                          │
│   Descrição em text-muted-foreground     │
│                                          │
│   [Comece grátis]  [Ver planos]          │
│                                          │
│   ✓ Sem cartão. Comece em 30s.           │
│   → Faça o diagnóstico gratuito          │
└─────────────────────────────────────────┘
```

- **Background glow:** `absolute w-96 h-96 bg-primary/20 rounded-full blur-3xl top-0 left-1/2 -translate-x-1/2`
- **Badge:** `rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm text-primary`
- **Headline:** `text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight`
- **Gradient text:** `bg-gradient-to-r from-primary via-emerald-400 to-primary bg-clip-text text-transparent`
- **CTA Primary:** `h-12 px-8 text-base rounded-lg bg-primary`
- **CTA Secondary:** `h-12 px-8 text-base rounded-lg variant="outline"`
- **Animação:** `animate-fade-in-up` com stagger delays (0.1s–0.5s)

### 5.3 Stats Bar

```
┌──────────┬──────────┬──────────┬──────────┐
│  +200    │    9     │  NPS 78  │   14     │
│ Empresas │  Partes  │ Satisf.  │  Dias    │
└──────────┴──────────┴──────────┴──────────┘
```

- **Layout:** `grid grid-cols-2 md:grid-cols-4 gap-4`
- **Card:** `rounded-xl border border-border bg-card/50 p-6 text-center`
- **Número:** `text-3xl font-bold text-primary`
- **Label:** `text-sm text-muted-foreground`
- **Animação:** `ScrollReveal` com stagger por índice

### 5.4 Framework Grid (9 Partes)

```
┌─────────┬─────────┬─────────┐
│ 01      │ 02      │ 03      │
│ ⏰ Tempo │ 👥 Deleg │ ➕ Contr │
│ Starter │ Starter │ Starter │
├─────────┼─────────┼─────────┤
│ 04      │ 05      │ 06      │
│ 🏢 Estr │ ⚙️ Proc │ 📅 Ritos │
│ Pro     │ Pro     │ Pro     │
├─────────┼─────────┼─────────┤
│ 07      │ 08      │ 09      │
│ 🎯 Proj │ ❤️ Pess │ 👑 Líder │
│ Enterpr │ Enterpr │ Enterpr │
└─────────┴─────────┴─────────┘
```

- **Grid:** `grid grid-cols-1 md:grid-cols-3 gap-4`
- **Card:** `rounded-xl border border-border p-6 bg-gradient-to-br {color} hover:border-foreground/20 transition-all group`
- **Número:** `text-xs font-mono text-muted-foreground` (formato "01")
- **Ícone:** `h-8 w-8 {iconColor} mb-3`
- **Título:** `font-semibold text-lg`
- **Tier badge:** `text-xs font-medium rounded-full px-2 py-0.5 bg-{color}/10 text-{color}`
- **Hover:** `hover:border-foreground/20` + `group-hover:scale-110` no ícone

### 5.5 Card Padrão (Feature/AI)

```
┌──────────────────────────┐
│ ⚡ Ícone                  │
│                           │
│ Título da Feature         │
│ Descrição curta em        │
│ muted-foreground          │
└──────────────────────────┘
```

- **Container:** `rounded-xl border border-border p-6 bg-card/50`
- **Ícone:** `h-10 w-10 text-primary mb-4` (Lucide React)
- **Título:** `font-semibold text-lg mb-2`
- **Descrição:** `text-sm text-muted-foreground`
- **Hover:** `hover:border-primary/20 transition-colors`

### 5.6 Comparison Row

```
┌───────────────────────────────────────────────┐
│  ✗ Planilhas espalhadas     ✓ Tudo centralizado │
│    text-red-400               text-primary      │
└───────────────────────────────────────────────┘
```

- **Layout:** `grid md:grid-cols-2 gap-4` por item
- **Negativo:** `X` icon `text-red-400` + texto `text-muted-foreground`
- **Positivo:** `Check` icon `text-primary` + texto `text-foreground`
- **Borda:** `border-b border-border py-4`

### 5.7 Testimonial Card

```
┌──────────────────────────────────┐
│ ★★★★★                            │
│                                   │
│ "Em 3 meses... consegui tirar    │
│ minhas primeiras |18h/semana|"   │
│                                   │
│ [RA] Rodrigo Almeida             │
│      CEO, TechNova · Tecnologia  │
│                              [in] │
└──────────────────────────────────┘
```

- **Container:** `rounded-xl border border-border p-6`
- **Stars:** `text-yellow-400 h-4 w-4` (Star icon filled)
- **Quote:** `text-muted-foreground text-sm` com métricas em `text-primary font-semibold`
- **Avatar:** `h-10 w-10 rounded-full bg-{color}/20 text-{color}` com iniciais
- **LinkedIn:** ícone externo link → abre nova aba

### 5.8 Pricing Card

```
┌──────────────────────┐
│  ┌─ POPULAR ─┐       │  ← only Pro
│                       │
│  Pro                  │
│  R$ 197/mês           │
│                       │
│  ✓ Partes 1-6         │
│  ✓ Até 20 membros     │
│  ✓ 80 análises IA/dia │
│  ✓ WhatsApp           │
│                       │
│  [Começar grátis]     │
└──────────────────────┘
```

- **Card:** `rounded-2xl border p-8`
- **Popular:** `border-primary glow-emerald` + badge absolute `-top-3`
- **Normal:** `border-border`
- **Preço:** `text-4xl font-bold` + `text-sm text-muted-foreground` ("/mês")
- **Features:** `Check h-4 w-4 text-primary` + `text-sm`
- **CTA Popular:** `bg-primary` (default)
- **CTA Normal:** `variant="outline"`

### 5.9 Badge

| Variante | Classe |
|----------|--------|
| Tier (hero) | `rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm text-primary` |
| Section label | `rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary` |
| Part tier | `text-xs rounded-full px-2 py-0.5 bg-{color}/10 text-{color}` |
| Popular | `bg-primary text-primary-foreground text-xs font-medium px-3 py-1 rounded-full` |

### 5.10 Button

| Variante | Classe | Uso |
|----------|--------|-----|
| Primary | `bg-primary text-primary-foreground hover:bg-primary/90 h-12 px-8 rounded-lg` | CTA principal |
| Outline | `border border-border bg-transparent hover:bg-foreground/5 h-12 px-8 rounded-lg` | CTA secundário |
| Ghost | `bg-transparent hover:bg-accent text-muted-foreground` | Nav links, login |
| Link | `text-primary hover:underline text-sm` | Inline links |

---

## 6. Animações

### Entrada (page load)

| Nome | Duração | Easing | Efeito |
|------|---------|--------|--------|
| `animate-fade-in-up` | 0.7s | ease-out | translateY(30→0) + opacity(0→1) |
| `animate-fade-in-left` | 0.7s | ease-out | translateX(-30→0) + opacity(0→1) |
| `animate-fade-in-right` | 0.7s | ease-out | translateX(30→0) + opacity(0→1) |

### Scroll Reveal (IntersectionObserver)

```css
.scroll-hidden → .scroll-visible
  opacity: 0→1
  translateY: 30px→0
  transition: 0.7s ease-out
```

- **Threshold:** 0.1
- **Root margin:** `0px 0px -50px 0px`
- **Stagger:** `.stagger-1` a `.stagger-9` (0.1s–0.9s delay)

### Contínuas

| Nome | Duração | Uso |
|------|---------|-----|
| `animate-gradient` | 6s infinite | Texto/fundo com gradient animado |
| `animate-float` | 3s ease-in-out infinite | Elementos decorativos flutuantes |
| `counter-pulse` | 0.5s | Pulso sutil em números ao aparecer |

---

## 7. Layout — Estrutura de Seções

### Ordem das 13 seções da homepage:

```
1.  HERO ─────────────── py-20 md:py-28, max-w-4xl
    │ headline + 2 CTAs + trust line
    │
2.  STATS ────────────── py-12, max-w-4xl
    │ 4 números em grid
    │
3.  FRAMEWORK ────────── py-20 md:py-28, max-w-6xl, id="framework"
    │ 9 cards em 3x3 grid
    │
4.  IA COMPLETA ──────── py-20 md:py-28, gradient bg
    │ badge + headline + 3 stats
    │ 6 AI category cards (3x2)
    │ mockup de demo
    │
5.  CONTRATAÇÃO ──────── py-20 md:py-28, max-w-6xl
    │ 6 feature cards + flow de 4 passos
    │
6.  COMPARAÇÃO ───────── py-20 md:py-28, max-w-4xl, id="comparacao"
    │ 6 linhas manual vs EI
    │
7.  FEATURES ─────────── py-20 md:py-28, max-w-5xl
    │ 6 cards em 3x2 grid
    │
8.  VERTICAIS ────────── py-20 md:py-28, max-w-4xl
    │ 6 segmentos com ícones
    │
9.  DEPOIMENTOS ──────── py-20 md:py-28, max-w-5xl
    │ social proof + 4 cards (2x2)
    │
10. PRICING ──────────── py-20 md:py-28, max-w-5xl
    │ 3 plans side by side
    │
11. FAQ ──────────────── py-20 md:py-28, max-w-3xl
    │ accordion
    │
12. DIAGNÓSTICO CTA ──── py-20 md:py-28, max-w-4xl
    │ gradient border card + CTA
    │
13. FINAL CTA ────────── py-20 md:py-28, max-w-3xl
    │ headline + 2 CTAs + glow
```

### Padrão de Seção

```html
<section className="py-20 md:py-28 px-4">
  <div className="max-w-{size} mx-auto">
    <!-- Badge (opcional) -->
    <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
      Label
    </span>

    <!-- Título -->
    <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-center mt-4 mb-4">
      Título da seção
    </h2>

    <!-- Subtítulo -->
    <p className="text-lg text-muted-foreground text-center max-w-2xl mx-auto mb-12 md:mb-16">
      Descrição
    </p>

    <!-- Conteúdo -->
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      ...
    </div>
  </div>
</section>
```

---

## 8. Responsividade

### Breakpoints

| Breakpoint | Largura | Comportamento |
|------------|---------|---------------|
| Mobile (default) | < 768px | 1 coluna, nav oculta, texto menor |
| `md:` | ≥ 768px | 2-3 colunas, nav visível, headlines maiores |
| `lg:` | ≥ 1024px | Headlines extra-grandes (7xl hero) |

### Grid Responsivo

| Seção | Mobile | Desktop |
|-------|--------|---------|
| Stats | `grid-cols-2` | `grid-cols-4` |
| Framework | `grid-cols-1` | `grid-cols-3` |
| AI Cards | `grid-cols-1` | `grid-cols-3` |
| Features | `grid-cols-1` | `grid-cols-3` |
| Verticais | `grid-cols-2` | `grid-cols-3` → `grid-cols-6` |
| Depoimentos | `grid-cols-1` | `grid-cols-2` |
| Pricing | `grid-cols-1` | `grid-cols-3` |

---

## 9. Footer

```
┌─────────────────────────────────────────────────────────┐
│ [EI] Empresa Independente                                │
│ Transforme sua empresa em um                             │
│ negócio independente.                                    │
│                                                          │
│ Produto        Empresa           Recursos                │
│ Método         Sobre nós         Diagnóstico gratuito    │
│ Preços         Termos de uso     Blog                    │
│ Começar grátis Política priv.    FAQ                     │
│                                  contato@empresaind.com  │
│                                                          │
│ ─────────────────────────────────────────────────────── │
│ © 2026 Empresa Independente. Todos os direitos reservados│
│ Feito com dedicação para empresários brasileiros. 🇧🇷    │
└─────────────────────────────────────────────────────────┘
```

- **Background:** `bg-card/50 border-t border-border`
- **Layout:** `grid grid-cols-2 md:grid-cols-4 gap-8`
- **Link hover:** `text-muted-foreground hover:text-primary transition-colors`
- **Copyright:** `text-xs text-muted-foreground border-t border-border pt-8`

---

## 10. Ícones

**Biblioteca:** Lucide React (`lucide-react`)

### Ícones por Contexto

| Contexto | Ícones |
|----------|--------|
| Framework Parts | Clock, Users, UserPlus, Building2, Workflow, CalendarCheck, Target, Heart, Crown |
| Features | Zap, BrainCircuit, Shield, Users, BarChart3, Sparkles |
| Navigation | Menu, X, ArrowRight, ExternalLink |
| Social Proof | Star (filled), Linkedin |
| Verticais | Store, Briefcase, Palette, GraduationCap, Stethoscope, ShoppingCart |
| Comparison | X (red), Check (green) |
| AI | Brain, Bot, Sparkles, FileText, LineChart, MessageSquare |

### Tamanhos Padrão

| Contexto | Classe |
|----------|--------|
| Inline (texto) | `h-4 w-4` |
| Card icon | `h-8 w-8` → `h-10 w-10` |
| Feature icon | `h-5 w-5` → `h-6 w-6` |
| Decorativo | `h-12 w-12` → `h-16 w-16` |

---

## 11. Arquivos de Referência

| Arquivo | Descrição |
|---------|-----------|
| `src/app/(marketing)/layout.tsx` | Header + Footer + dark theme |
| `src/app/(marketing)/page.tsx` | Metadata + structured data |
| `src/components/marketing/home-page-content.tsx` | 13 seções (949 linhas) |
| `src/components/marketing/scroll-reveal.tsx` | Animação scroll |
| `src/components/marketing/faq-section.tsx` | FAQ accordion |
| `src/components/marketing/mobile-nav.tsx` | Nav mobile |
| `src/app/globals.css` | Cores, animações, glow effects |
| `src/lib/faq-data.ts` | Dados do FAQ |
| `src/lib/constants.ts` | Planos, limites, tiers |
