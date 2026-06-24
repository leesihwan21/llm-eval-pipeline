import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [prompt, setPrompt] = useState("");
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    const res = await axios.get(`${API_URL}/api/eval/history`);
    setHistory(res.data.history);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const runEval = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/api/eval/run`, {
        prompt,
        models: ["claude-sonnet-4-6"],
        task_type: "general",
      });
      setResults(res.data.results);
      fetchHistory();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 32, fontFamily: "sans-serif" }}>
      <h1>🧪 LLM Eval Pipeline</h1>

      <div style={{ marginBottom: 24 }}>
        <textarea
          rows={4}
          style={{ width: "100%", padding: 12, fontSize: 16, borderRadius: 8, border: "1px solid #ccc" }}
          placeholder="평가할 프롬프트를 입력하세요..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button
          onClick={runEval}
          disabled={loading}
          style={{ marginTop: 8, padding: "12px 24px", fontSize: 16, background: "#6366f1", color: "white", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "평가 중..." : "평가 실행"}
        </button>
      </div>

      {results.length > 0 && (
        <div style={{ marginBottom: 32 }}>
          <h2>📊 평가 결과</h2>
          {results.map((r, i) => (
            <div key={i} style={{ background: "#f8f8f8", padding: 16, borderRadius: 8, marginBottom: 12 }}>
              <b>{r.model_name}</b> | 점수: <b>{r.score}</b> | 응답시간: {r.latency_ms}ms
              <p style={{ marginTop: 8 }}>{r.response}</p>
            </div>
          ))}
        </div>
      )}

      <div>
        <h2>📜 평가 히스토리</h2>
        {history.map((h, i) => (
          <div key={i} style={{ background: "#f0f0f0", padding: 12, borderRadius: 8, marginBottom: 8 }}>
            <b>{h.model_name}</b> | 점수: {h.score} | {h.created_at}
            <p style={{ margin: "4px 0" }}>프롬프트: {h.prompt}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;