export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { user_id } = req.body;
    if (!user_id) {
      return res.status(400).json({ error: "Missing user_id" });
    }

    // Отправляем запрос на Render
    const response = await fetch("https://telega-6jtc.onrender.com/create_invoice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      return res.status(500).json({
        error: "Render error",
        details: data,
      });
    }

    return res.status(200).json({ status: "ok" });
  } catch (err) {
    console.error("Invoice API error:", err);
    return res.status(500).json({ error: "Server error" });
  }
}
