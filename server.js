const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const os = require('os');

const app = express();
app.use(express.json({ limit: '10mb' }));
app.use(express.static(__dirname));

const ROOT = __dirname;
const UPLOADS_DIR = path.join(os.tmpdir(), 'prompt-studio-uploads');
if (!fs.existsSync(UPLOADS_DIR)) fs.mkdirSync(UPLOADS_DIR, { recursive: true });

const CLAUDE_CLI_JS = 'C:\\Users\\Gabriel\\AppData\\Roaming\\npm\\node_modules\\@anthropic-ai\\claude-code\\cli.js';

// ─── Multer storage ───
const storage = multer.diskStorage({
  destination: UPLOADS_DIR,
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname.replace(/[^a-zA-Z0-9._-]/g, '_')}`),
});
const upload = multer({ storage, limits: { fileSize: 20 * 1024 * 1024 } }); // 20MB

// ─── File helpers ───
function readFolder(folderPath) {
  const abs = path.join(ROOT, folderPath);
  if (!fs.existsSync(abs)) return [];
  const results = [];
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      const ext = path.extname(entry.name).toLowerCase();
      if (['.md', '.txt'].includes(ext)) {
        try {
          const content = fs.readFileSync(full, 'utf-8');
          results.push({ file: path.relative(ROOT, full).replace(/\\/g, '/'), content });
        } catch { }
      }
    }
  }
  walk(abs);
  return results;
}

function readSkill(skillName) {
  const p = path.join(ROOT, '.claude', 'skills', skillName, 'SKILL.md');
  return fs.existsSync(p) ? fs.readFileSync(p, 'utf-8') : null;
}

const truncate = (text, limit) =>
  text.length > limit
    ? text.slice(0, limit) + `\n\n[... ${text.length - limit} chars omitidos]`
    : text;

// ─── Extract text from uploaded file ───
async function extractText(filePath, mimetype, originalname) {
  const ext = path.extname(originalname).toLowerCase();

  // PDF
  if (ext === '.pdf' || mimetype === 'application/pdf') {
    try {
      const pdfParse = require('pdf-parse');
      const data = await pdfParse(fs.readFileSync(filePath));
      return { type: 'text', content: data.text };
    } catch (e) {
      return { type: 'text', content: `[PDF não pôde ser extraído: ${e.message}]` };
    }
  }

  // Plain text / code / markdown
  const textExts = ['.txt', '.md', '.csv', '.json', '.js', '.ts', '.py', '.html', '.css', '.xml', '.yaml', '.yml'];
  if (textExts.includes(ext)) {
    return { type: 'text', content: fs.readFileSync(filePath, 'utf-8') };
  }

  // Images
  const imageExts = ['.png', '.jpg', '.jpeg', '.gif', '.webp'];
  if (imageExts.includes(ext) || mimetype?.startsWith('image/')) {
    return { type: 'image', path: filePath, name: originalname };
  }

  return { type: 'unknown', content: `[Arquivo não suportado: ${originalname}]` };
}

// ─── Upload endpoint ───
app.post('/api/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'no file' });
  try {
    const result = await extractText(req.file.path, req.file.mimetype, req.file.originalname);
    res.json({
      id: req.file.filename,
      name: req.file.originalname,
      size: req.file.size,
      ...result,
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ─── Delete upload ───
app.delete('/api/upload/:id', (req, res) => {
  const p = path.join(UPLOADS_DIR, req.params.id);
  if (fs.existsSync(p)) fs.unlinkSync(p);
  res.json({ ok: true });
});

// ─── List skills ───
app.get('/api/skills', (req, res) => {
  const dir = path.join(ROOT, '.claude', 'skills');
  if (!fs.existsSync(dir)) return res.json([]);
  res.json(fs.readdirSync(dir, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name));
});

// ─── Run claude CLI ───
function runClaude(fullPrompt, imageFiles = []) {
  return new Promise((resolve, reject) => {
    const childEnv = { ...process.env };
    delete childEnv.CLAUDECODE;
    delete childEnv.CLAUDE_CODE;

    const args = ['--print', '--output-format', 'text'];
    for (const imgPath of imageFiles) {
      if (fs.existsSync(imgPath)) args.push('--file', imgPath);
    }

    const proc = spawn(process.execPath, [CLAUDE_CLI_JS, ...args], {
      cwd: ROOT, env: childEnv, stdio: ['pipe', 'pipe', 'pipe'],
    });

    let out = '', err = '';
    proc.stdin.write(fullPrompt, 'utf-8');
    proc.stdin.end();
    proc.stdout.on('data', c => { out += c.toString('utf-8'); });
    proc.stderr.on('data', c => { err += c.toString('utf-8'); });
    proc.on('close', code => {
      if (code !== 0 && !out) reject(new Error(err.trim() || `Exit code ${code}`));
      else resolve(out);
    });
    proc.on('error', reject);
  });
}

// ─── Generate ───
app.post('/api/generate', async (req, res) => {
  const { prompt, skills = [], folders = [], attachments = [] } = req.body;
  if (!prompt) return res.status(400).json({ error: 'prompt required' });

  const MAX_SKILL = 6000, MAX_FILE = 4000, MAX_TOTAL = 40000;
  const parts = [];
  const imageFiles = [];

  // Skills
  if (skills.length > 0) {
    parts.push('# SKILLS ATIVAS\n');
    for (const skill of skills) {
      const content = readSkill(skill);
      if (content) parts.push(`## SKILL: ${skill}\n\n${truncate(content, MAX_SKILL)}`);
    }
  }

  // Folders
  if (folders.length > 0) {
    parts.push('# ARQUIVOS DO PROJETO\n');
    for (const folder of folders) {
      for (const { file, content } of readFolder(folder)) {
        parts.push(`## ${file}\n\`\`\`\n${truncate(content, MAX_FILE)}\n\`\`\``);
      }
    }
  }

  // Attachments
  if (attachments.length > 0) {
    const textAttachments = attachments.filter(a => a.type === 'text');
    const imgAttachments  = attachments.filter(a => a.type === 'image');

    if (textAttachments.length > 0) {
      parts.push('# DOCUMENTOS ANEXADOS\n');
      for (const att of textAttachments) {
        parts.push(`## ${att.name}\n\`\`\`\n${truncate(att.content || '', MAX_FILE)}\n\`\`\``);
      }
    }

    if (imgAttachments.length > 0) {
      parts.push(`# IMAGENS ANEXADAS\n${imgAttachments.map(a => `- ${a.name}`).join('\n')}\n(imagens enviadas como arquivos para análise visual)`);
      for (const att of imgAttachments) {
        if (att.path) imageFiles.push(att.path);
      }
    }
  }

  // Audio transcription (sent as text from browser)
  if (req.body.audioTranscript) {
    parts.push(`# TRANSCRIÇÃO DE ÁUDIO\n${req.body.audioTranscript}`);
  }

  parts.push(`# SOLICITAÇÃO\n\n${prompt}`);
  let fullPrompt = parts.join('\n\n---\n\n');

  if (fullPrompt.length > MAX_TOTAL) {
    const tail = `# SOLICITAÇÃO\n\n${prompt}`;
    fullPrompt = `[Contexto truncado — ${fullPrompt.length} chars → ${MAX_TOTAL}]\n\n` +
      parts.slice(0, 2).join('\n\n---\n\n') + '\n\n---\n\n' + tail;
  }

  // SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const send = (event, data) => res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
  send('heartbeat', { status: 'running' });

  try {
    const output = await runClaude(fullPrompt, imageFiles);
    const CHUNK = 60;
    for (let i = 0; i < output.length; i += CHUNK) {
      send('delta', { text: output.slice(i, i + CHUNK) });
    }
    send('done', {});
  } catch (e) {
    send('error', { message: e.message });
  }

  res.end();
});

// ─── Save output ───
app.post('/api/save', (req, res) => {
  const { content, filename } = req.body;
  if (!content) return res.status(400).json({ error: 'content required' });
  const name = ((filename || `output-${Date.now()}`).replace(/[^a-zA-Z0-9\-_. ]/g, '').replace(/\s+/g, '-').trim() || 'output') + (filename?.endsWith('.md') ? '' : '.md');
  fs.writeFileSync(path.join(ROOT, 'EI', name), content, 'utf-8');
  res.json({ saved: `EI/${name}` });
});

app.get('/prompt-builder', (req, res) => res.redirect('/prompt-builder.html'));
app.get('/', (req, res) => res.redirect('/prompt-builder.html'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`\n  Prompt Studio → http://localhost:${PORT}\n`));
