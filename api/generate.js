// Vercel Serverless Function — /api/generate (SSE streaming)
// Porta a logica de montagem de prompt do server.js, mas SEMPRE usa o
// Anthropic SDK (nunca o CLI local claude.exe, que nao existe em producao).
// Mantem o MESMO protocolo SSE consumido pelo frontend (prompt-builder.html):
//   eventos: heartbeat, step, progress, log, skill-loaded, delta, warning, error, done

import fs from 'fs';
import path from 'path';
import Anthropic from '@anthropic-ai/sdk';

const ROOT = process.cwd();

// ─── File helpers (somente leitura — ok em filesystem read-only da Vercel) ───
function readFolder(folderPath) {
  const abs = path.join(ROOT, folderPath);
  if (!fs.existsSync(abs)) return [];
  const results = [];
  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
        continue;
      }
      const ext = path.extname(entry.name).toLowerCase();
      if (['.md', '.txt'].includes(ext)) {
        try {
          const content = fs.readFileSync(full, 'utf-8');
          results.push({ file: path.relative(ROOT, full).replace(/\\/g, '/'), content });
        } catch {}
      }
    }
  }
  walk(abs);
  return results;
}

function readSkill(skillName) {
  const p = path.join(ROOT, '.claude', 'skills', skillName, 'SKILL.md');
  try {
    return fs.existsSync(p) ? fs.readFileSync(p, 'utf-8') : null;
  } catch {
    return null;
  }
}

const truncate = (text, limit) =>
  text.length > limit
    ? text.slice(0, limit) + `\n\n[... ${text.length - limit} chars omitidos]`
    : text;

// ─── Geracao via Anthropic SDK (streaming) — com suporte a imagens base64 ───
async function runAnthropicSDK(fullPrompt, imageBlocks, send) {
  const client = new Anthropic();

  const content = [];
  for (const block of imageBlocks) content.push(block);
  content.push({ type: 'text', text: fullPrompt });

  send('log', { text: `Anthropic SDK iniciado (com ${imageBlocks.length} imagem/ns)` });
  send('step', { index: 5, label: 'Executando Claude (SDK)...', total: 6 });
  send('progress', { percent: 60, label: 'Claude SDK iniciado' });

  let out = '';
  let chunkCount = 0;

  const stream = client.messages.stream({
    model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-6',
    max_tokens: 8192,
    messages: [{ role: 'user', content }],
  });

  for await (const event of stream) {
    if (event.type === 'content_block_delta' && event.delta?.type === 'text_delta') {
      const text = event.delta.text;
      out += text;
      chunkCount++;
      send('delta', { text });
      const streamProgress = Math.min(95, 60 + Math.floor(chunkCount * 0.5));
      send('progress', { percent: streamProgress, label: 'Recebendo resposta...' });
      if (chunkCount === 1) {
        send('step', { index: 6, label: 'Recebendo resposta...', total: 6 });
      }
    }
  }

  send('progress', { percent: 100, label: 'Concluido' });
  return out;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { prompt, skills = [], folders = [], attachments = [], messages = [] } = req.body || {};
  if (!prompt) return res.status(400).json({ error: 'prompt required' });

  // SSE setup
  res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache, no-transform');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');
  if (typeof res.flushHeaders === 'function') res.flushHeaders();

  const send = (event, data) => res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
  send('heartbeat', { status: 'running' });

  const MAX_SKILL = 6000,
    MAX_FILE = 4000,
    MAX_TOTAL = 40000;
  const parts = [];
  const imageBlocks = [];

  // Step 1: Skills
  send('step', { index: 1, label: 'Carregando skills...', total: 6 });
  if (skills.length > 0) {
    parts.push('# SKILLS ATIVAS\n');
    for (const skill of skills) {
      const content = readSkill(skill);
      if (content) {
        parts.push(`## SKILL: ${skill}\n\n${truncate(content, MAX_SKILL)}`);
        const size = Buffer.byteLength(content, 'utf-8');
        send('log', { text: `Skill carregada: ${skill} (${(size / 1024).toFixed(1)} KB)` });
        send('skill-loaded', { name: skill, size });
      } else {
        send('log', { text: `Skill nao encontrada no bundle: ${skill}` });
      }
    }
  }
  send('progress', { percent: 10, label: 'Skills carregadas' });

  // Step 2: Folders
  send('step', { index: 2, label: 'Lendo pastas de contexto...', total: 6 });
  if (folders.length > 0) {
    parts.push('# ARQUIVOS DO PROJETO\n');
    for (const folder of folders) {
      const files = readFolder(folder);
      send('log', { text: `Pasta lida: ${folder} (${files.length} arquivos)` });
      for (const { file, content } of files) {
        parts.push(`## ${file}\n\`\`\`\n${truncate(content, MAX_FILE)}\n\`\`\``);
      }
    }
  }
  send('progress', { percent: 30, label: 'Pastas lidas' });

  // Step 3: Attachments (texto inline + imagens via base64)
  send('step', { index: 3, label: 'Processando anexos...', total: 6 });
  if (attachments.length > 0) {
    const textAttachments = attachments.filter((a) => a.type === 'text');
    const imgAttachments = attachments.filter((a) => a.type === 'image');

    if (textAttachments.length > 0) {
      parts.push('# DOCUMENTOS ANEXADOS\n');
      for (const att of textAttachments) {
        parts.push(`## ${att.name}\n\`\`\`\n${truncate(att.content || '', MAX_FILE)}\n\`\`\``);
      }
    }

    if (imgAttachments.length > 0) {
      parts.push(
        `# IMAGENS ANEXADAS\n${imgAttachments.map((a) => `- ${a.name}`).join('\n')}\n(imagens enviadas como arquivos para analise visual)`
      );
      for (const att of imgAttachments) {
        if (att.content) {
          const mediaType = att.mediaType || 'image/png';
          imageBlocks.push({
            type: 'image',
            source: { type: 'base64', media_type: mediaType, data: att.content },
          });
        }
      }
    }
    send('log', { text: `Anexos processados: ${attachments.length} arquivo(s)` });
  }
  send('progress', { percent: 45, label: 'Anexos processados' });

  // Audio transcription
  if (req.body.audioTranscript) {
    parts.push(`# TRANSCRIÇÃO DE ÁUDIO\n${req.body.audioTranscript}`);
  }

  // Conversation history
  if (messages.length > 0) {
    const history = messages
      .map((m) => `${m.role === 'user' ? 'Usuário' : 'Assistente'}: ${m.content}`)
      .join('\n\n');
    parts.push(`# HISTÓRICO DA CONVERSA\n\n${history}`);
  }

  // Step 4: Mount prompt
  send('step', { index: 4, label: 'Montando prompt...', total: 6 });
  parts.push(`# ${messages.length > 0 ? 'NOVA MENSAGEM' : 'SOLICITAÇÃO'}\n\n${prompt}`);
  let fullPrompt = parts.join('\n\n---\n\n');

  const originalSize = fullPrompt.length;
  if (fullPrompt.length > MAX_TOTAL) {
    const tail = `# SOLICITAÇÃO\n\n${prompt}`;
    fullPrompt =
      `[Contexto truncado — ${fullPrompt.length} chars → ${MAX_TOTAL}]\n\n` +
      parts.slice(0, 2).join('\n\n---\n\n') +
      '\n\n---\n\n' +
      tail;
    send('warning', {
      type: 'truncated',
      originalSize,
      truncatedTo: MAX_TOTAL,
      message: `Contexto truncado: ${originalSize.toLocaleString()} → ${MAX_TOTAL.toLocaleString()} chars`,
    });
    send('log', { text: `AVISO: Contexto truncado de ${originalSize} para ${MAX_TOTAL} caracteres` });
  }

  send('log', { text: `Prompt montado: ${fullPrompt.length} caracteres` });
  send('progress', { percent: 55, label: 'Prompt montado' });

  // Step 5-6: Run via Anthropic SDK (sempre)
  try {
    if (!process.env.ANTHROPIC_API_KEY) {
      throw new Error(
        'ANTHROPIC_API_KEY nao configurada no ambiente de producao da Vercel. ' +
          'Configure em Settings > Environment Variables (Production) e faca redeploy.'
      );
    }
    await runAnthropicSDK(fullPrompt, imageBlocks, send);
    send('done', {});
  } catch (e) {
    send('error', { message: e.message });
  }

  res.end();
}
