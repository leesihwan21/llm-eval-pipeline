import { useState, useEffect } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const API_URL = "http://127.0.0.1:8000";

const MODELS = [
  { id: "claude-sonnet-4-6", label: "Claude Sonnet 4.6" },
  { id: "gpt-4o-mini", label: "GPT-4o Mini" },
];

function App() {
  const [prompt, setPrompt] = useState("");
  const [selectedModels, setSelectedModels] = useState(["claude-sonnet-4-6"]);
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

  const toggleModel = (id) => {
    setSelectedModels((prev) =>
      prev.includes(id) ? prev.filter((m) => m !== id) : [...prev, id]
    );
  };

  const runEval = async () => {
    if (!prompt || selectedModels.length === 0) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/api/eval/run`, {
        prompt,
        models: selectedModels,
        task_type: "general",
      });
      setResults(res.data.results);
      fetchHistory();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const chartData = results.map((r) => ({
    name: r.model_name,
    점수: r.score,
    응답시간: Math.round(r.latency_ms / 100) / 10,
  }));

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-purple-400">
          🧪 LLM Eval Pipeline
        </h1>

        <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
          <textarea
            rows={4}
            className="w-full bg-gray-800 text-white rounded-lg p-4 text-base border border-gray-700 focus:outline-none focus:border-purple-500 resize-none"
            placeholder="평가할 프롬프트를 입력하세요..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <div className="flex gap-3 mt-4 mb-4">
            {MODELS.map((m) => (
              <button
                key={m.id}
                onClick={() => toggleModel(m.id)}
                className={`px-4 py-2 rounded-lg text-sm font-semibold border transition ${
                  selectedModels.includes(m.id)
                    ? "bg-purple-600 border-purple-500 text-white"
                    : "bg-gray-800 border-gray-600 text-gray-400"
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
          <button
            onClick={runEval}
            disabled={loading}
            className="w-full py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 text-white font-semibold rounded-lg transition"
          >
            {loading ? "⏳ 평가 중..." : "🚀 평가 실행"}
          </button>
        </div>

        {results.length > 0 && (
          <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
            <h2 className="text-xl font-bold text-purple-400 mb-4">📊 평가 결과</h2>
            {results.map((r, i) => (
              <div key={i} className="bg-gray-800 rounded-lg p-4 mb-3">
                <div className="flex gap-4 text-sm text-gray-400 mb-2">
                  <span className="text-purple-400 font-semibold">{r.model_name}</span>
                  <span>점수: <b className="text-white">{r.score}</b></span>
                  <span>응답시간: {r.latency_ms}ms</span>
                </div>
                <p className="text-gray-200 text-sm leading-relaxed">{r.response}</p>
              </div>
            ))}

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-purple-400 mb-3">📈 모델 비교 차트</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
                  <Legend />
                  <Bar dataKey="점수" fill="#8b5cf6" />
                  <Bar dataKey="응답시간(초)" fill="#06b6d4" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-purple-400 mb-4">📜 평가 히스토리</h2>
          {history.length === 0 && <p className="text-gray-500">히스토리가 없어요.</p>}
          {history.map((h, i) => (
            <div key={i} className="bg-gray-800 rounded-lg p-4 mb-3">
              <div className="flex gap-4 text-sm text-gray-400 mb-1">
                <span className="text-purple-400 font-semibold">{h.model_name}</span>
                <span>점수: <b className="text-white">{h.score}</b></span>
                <span>{h.created_at}</span>
              </div>
              <p className="text-gray-300 text-sm">프롬프트: {h.prompt}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;