export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const { user_id, init_data } = req.body;
  if (!user_id) return res.status(400).json({ error: "Missing user_id" });

  try {
    const botUrl = "https://telega-6jtc.onrender.com/create_invoice";

    const response = await fetch(botUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id, init_data }),
    });

    const result = await response.json();
    res.status(200).json(result);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to contact bot" });
  }
}
