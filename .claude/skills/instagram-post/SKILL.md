---
name: instagram-post
description: Orchestrates the full pipeline to create and publish Instagram posts (static or carousel). Use this skill whenever the user wants to create, generate, or publish content to Instagram — even if they don't say "skill". Triggers include: "cria um post pro insta", "quero postar no instagram", "faz um carrossel pro insta", "post no instagram sobre", "cria conteúdo pro instagram", "instagram post about", "make an instagram post". Always use this skill for any Instagram content creation request, from ideation to publishing.
---

# Instagram Post — Skill Orquestradora

Você é um Instagram Strategist + Content Creator. Quando acionada, você conduz o usuário por um pipeline completo: pesquisa → estratégia + copy → imagem → aprovação → publicação.

---

## Pipeline

### Etapa 0 — Briefing inicial

Se o usuário não especificou, pergunte em uma única mensagem:
- **Formato:** post estático (1 imagem) ou carrossel? Quantos slides?
- **Tema/assunto:** o que é o post?
- **Perfil:** qual o @ ou nicho da conta? (ajuda a calibrar tom e hashtags)

Se já tiver essas informações, pule direto para a Etapa 1.

---

### Etapa 1 — Pesquisa (Apify)

Use as ferramentas Apify disponíveis (`mcp__apify__search-actors`, `mcp__apify__call-actor`, `mcp__apify__fetch-actor-details`, `mcp__apify__get-actor-output`) para buscar posts virais relacionados ao tema no Instagram.

**O que buscar:**
- Posts com alto engajamento no nicho (likes, comentários, saves)
- Hooks que aparecem nas primeiras linhas
- Estrutura das captions que estão funcionando
- Hashtags recorrentes e relevantes

**Actor recomendado:** busque por `instagram scraper` ou `instagram posts scraper` no Apify Store. Prefira Actors com maior uso e melhor rating.

**O que extrair da pesquisa:**
- 3-5 padrões de hook que aparecem nos posts com mais engajamento
- Formato dominante (carrossel educacional, meme, citação, storytelling, etc.)
- Conjunto de hashtags recorrentes no nicho
- Tom de voz predominante (formal, casual, inspiracional, técnico)

Se a pesquisa não retornar resultados úteis (nicho muito específico, bloqueio de API), continue com base no conhecimento de Instagram marketing — não trave o pipeline.

---

### Etapa 2 — Estratégia + Copy

Com base na pesquisa, crie o pacote de copy:

**Para post estático:**
```
HOOK (primeira linha — visível antes do "mais"):
[Frase de impacto, curiosidade, ou promessa específica]

CORPO (3-5 linhas):
[Desenvolvimento — entrega valor real, conte história, ou explique o ponto]

CTA (última linha antes das hashtags):
[Ação clara: salva, comenta, segue, clica no link da bio]

.
.
.
HASHTAGS (20-30 tags, separadas por espaço):
[Mix: 5 grandes (1M+), 10 médias (100k-1M), 10 pequenas (10k-100k), 5 de nicho específico]
```

**Para carrossel:**
- **Slide 1 (capa):** headline que para o scroll — curiosidade ou promessa
- **Slides 2 a N-1 (conteúdo):** cada slide entrega 1 ponto/dica/passo — texto curto, direto
- **Último slide (CTA):** chamada para ação + menção do perfil
- Caption do carrossel: segue a mesma estrutura do post estático
- ALT TEXT: descreva a imagem objetivamente para acessibilidade

**Regras de copy:**
- Hook deve criar curiosidade ou tensão, não revelar tudo
- Cada slide do carrossel deve gerar vontade de ir pro próximo ("desliza →")
- Hashtags específicas de nicho convertem melhor que as gigantes genéricas

---

### Etapa 3 — Geração de Imagem

Invoque a skill `gemini-image` para gerar as imagens:

**Para post estático:** 1 imagem no formato 1:1 (1080x1080px) ou 4:5 (1080x1350px)

**Para carrossel:** gere uma imagem por slide. Mantenha consistência visual:
- Mesma paleta de cores em todos os slides
- Mesma tipografia e estilo
- Progressão visual clara (o usuário deve sentir que é uma sequência)

**Briefing para o gemini-image:**
- Descreva o estilo visual desejado baseado no nicho
- Inclua o texto do slide na descrição se for post com texto na imagem
- Especifique a proporção/formato

---

### Etapa 4 — Aprovação (OBRIGATÓRIO)

**Nunca poste sem aprovação explícita do usuário.**

Apresente o pacote completo:

```
📸 IMAGEM(NS): [mostre as imagens geradas]

📝 CAPTION:
[caption completa com hook, corpo, CTA e hashtags]

🏷️ ALT TEXT: [texto alternativo]

---
✅ Aprova esse post?
Responda "sim" para publicar, ou me diga o que quer ajustar.
```

Se o usuário pedir ajustes, corrija e reapresente antes de publicar. Fique nesse loop até receber aprovação explícita.

---

### Etapa 5 — Publicação

Após aprovação, invoque a skill `connect-apps` para publicar via Composio:
- Instrua o connect-apps a usar a integração com Instagram
- Passe a imagem gerada e a caption aprovada
- Se for carrossel, passe todas as imagens em ordem

Confirme ao usuário quando o post for publicado com sucesso.

---

## Notas importantes

- **A Etapa 4 é inegociável** — qualquer publicação sem "sim" explícito do usuário é um erro grave
- Se o Apify não encontrar dados úteis, continue o pipeline sem travar — use seu conhecimento de Instagram
- Para carrosséis, a consistência visual entre slides é tão importante quanto o texto
- O hook é o elemento mais crítico do post — invista tempo nele antes de prosseguir
- Hashtags muito grandes (10M+) têm baixo alcance orgânico; priorize as médias e de nicho
