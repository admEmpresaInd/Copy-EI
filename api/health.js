// Vercel Serverless Function — /api/health
// Substitui a checagem do binario claude.exe local (que so existe na maquina
// do dev) por uma checagem da env var ANTHROPIC_API_KEY, usada pelo SDK em prod.

export default async function handler(req, res) {
  try {
    const hasKey = !!process.env.ANTHROPIC_API_KEY;
    if (!hasKey) {
      return res.status(200).json({
        ok: false,
        message:
          'ANTHROPIC_API_KEY nao configurada. Defina em Vercel > Settings > Environment Variables (Production).',
      });
    }
    return res.status(200).json({
      ok: true,
      version: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-6',
      message: 'API Anthropic configurada',
    });
  } catch (e) {
    return res.status(200).json({ ok: false, message: e.message || 'Erro no health check' });
  }
}
