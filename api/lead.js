export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, phone, email, tags, source } = req.body;

  if (!name || !phone) {
    return res.status(400).json({ error: 'name e phone são obrigatórios' });
  }

  try {
    const response = await fetch('https://crm-ei.vercel.app/api/leads/inbound', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.CRM_EI_API_KEY,
      },
      body: JSON.stringify({ name, phone, email, tags, source }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json(data);
    }

    return res.status(response.status).json(data);
  } catch (err) {
    return res.status(500).json({ error: 'Erro interno ao contatar o CRM' });
  }
}
