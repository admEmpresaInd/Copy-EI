// Vercel Serverless Function — /api/upload (multipart/form-data)
// Em producao serverless o filesystem e efemero e nao e compartilhado entre
// invocacoes (upload e generate rodam em lambdas distintas). Por isso NAO
// gravamos em disco: extraimos o conteudo em memoria e devolvemos direto ao
// cliente (texto extraido para docs, base64 para imagens). O generate recebe
// esse conteudo de volta no corpo da requisicao.

import path from 'path';
import Busboy from 'busboy';

// Vercel nao faz parse de multipart/form-data — o stream fica disponivel em req.

function parseMultipart(req) {
  return new Promise((resolve, reject) => {
    let bb;
    try {
      bb = Busboy({ headers: req.headers, limits: { fileSize: 20 * 1024 * 1024 } });
    } catch (e) {
      return reject(e);
    }
    let fileBuffer = null;
    let fileInfo = null;
    let tooBig = false;

    bb.on('file', (_name, stream, info) => {
      const chunks = [];
      stream.on('data', (d) => chunks.push(d));
      stream.on('limit', () => {
        tooBig = true;
        stream.resume();
      });
      stream.on('end', () => {
        fileBuffer = Buffer.concat(chunks);
        fileInfo = info;
      });
    });
    bb.on('error', reject);
    bb.on('close', () => {
      if (tooBig) return reject(new Error('Arquivo excede o limite de 20MB'));
      resolve({ fileBuffer, fileInfo });
    });
    req.pipe(bb);
  });
}

async function extractText(buffer, mimetype, originalname) {
  const ext = path.extname(originalname).toLowerCase();

  // PDF (pdf-parse v2: classe PDFParse)
  if (ext === '.pdf' || mimetype === 'application/pdf') {
    try {
      const mod = await import('pdf-parse');
      const PDFParse = mod.PDFParse || mod.default?.PDFParse;
      const parser = new PDFParse({ data: buffer });
      const result = await parser.getText();
      return { type: 'text', content: result.text };
    } catch (e) {
      return { type: 'text', content: `[PDF não pôde ser extraído: ${e.message}]` };
    }
  }

  // Texto / codigo / markdown
  const textExts = [
    '.txt', '.md', '.csv', '.json', '.js', '.ts', '.py',
    '.html', '.css', '.xml', '.yaml', '.yml',
  ];
  if (textExts.includes(ext)) {
    return { type: 'text', content: buffer.toString('utf-8') };
  }

  // Imagens — devolve base64 (consumido pelo /api/generate)
  const imageExts = ['.png', '.jpg', '.jpeg', '.gif', '.webp'];
  const mimeMap = {
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp',
  };
  if (imageExts.includes(ext) || mimetype?.startsWith('image/')) {
    return {
      type: 'image',
      content: buffer.toString('base64'),
      mediaType: mimeMap[ext] || mimetype || 'image/png',
    };
  }

  return { type: 'unknown', content: `[Arquivo não suportado: ${originalname}]` };
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  try {
    const { fileBuffer, fileInfo } = await parseMultipart(req);
    if (!fileBuffer || !fileInfo) return res.status(400).json({ error: 'no file' });

    const originalname = fileInfo.filename || 'arquivo';
    const mimetype = fileInfo.mimeType || fileInfo.mimetype || '';
    const result = await extractText(fileBuffer, mimetype, originalname);

    const id = `${Date.now()}-${originalname.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
    return res.status(200).json({
      id,
      name: originalname,
      size: fileBuffer.length,
      ...result,
    });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
