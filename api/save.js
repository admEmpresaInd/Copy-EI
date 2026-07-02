// Vercel Serverless Function — /api/save
// Em producao serverless o filesystem e read-only (exceto /tmp, que nao
// persiste). Logo, NAO gravamos no projeto como o server.js faz localmente.
// Em vez disso devolvemos o conteudo para o navegador fazer o download.
// O frontend (prompt-builder.html) detecta a ausencia de `saved` e dispara
// o download do arquivo.

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { content, filename, html } = req.body || {};
  if (!content) return res.status(400).json({ error: 'content required' });

  const ext = html ? '.html' : '.md';
  const base =
    (filename || `output-${Date.now()}`)
      .replace(/[^a-zA-Z0-9\-_. ]/g, '')
      .replace(/\s+/g, '-')
      .trim() || 'output';
  const name = base.endsWith(ext) ? base : base.replace(/\.(md|html)$/, '') + ext;

  return res.status(200).json({
    download: true,
    filename: name,
    content,
    mime: html ? 'text/html' : 'text/markdown',
  });
}
