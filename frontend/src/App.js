import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");

  const handleCheck = async () => {
    // VERY SIMPLE feature extraction (for now)
    const features = [
      url.length,
      (url.match(/\./g) || []).length,
      url.includes("@") ? 1 : 0,
      url.startsWith("https") ? 1 : 0,
    ];

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ features }),
    });

    const data = await response.json();

    setResult(data.prediction === 1 ? "⚠️ Phishing" : "✅ Safe");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>PhishNet 🔐</h1>

      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={handleCheck} style={{ padding: "10px 20px" }}>
        Check URL
      </button>

      <h2>{result}</h2>
    </div>
  );
}

export default App;