// Vercel Serverless Function — /api/upload/:id (DELETE)
// Em producao os anexos nao sao gravados em disco (ver api/upload.js), entao
// nao ha arquivo temporario para remover. Mantemos a rota para preservar o
// contrato do frontend (fetch('/api/upload/' + id, { method: 'DELETE' })).

export default async function handler(req, res) {
  if (req.method !== 'DELETE') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  // No-op: nada persistido no servidor. O frontend remove do estado local.
  return res.status(200).json({ ok: true });
}
