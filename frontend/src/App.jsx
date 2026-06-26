import { useState, useEffect } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from "recharts";

const API_URL = "http://127.0.0.1:8000";

const MODELS = [
  { id: "claude-sonnet-4-6", label: "Claude Sonnet 4.6" },
  { id: "gpt-4o-mini", label: "GPT-4o Mini" },
  { id: "gemini-1.5-flash", label: "Gemini 1.5 Flash" },
];

const METRIC_COLORS = {
  llm_score: "#8b5cf6",
  rouge1: "#06b6d4",
  rouge2: "#10b981",
  rougeL: "#f59e0b",
};

function App() {
  const [tab, setTab] = useState("single"); // "single" | "batch"
  const [prompt, setPrompt] = useState("");
  const [batchText, setBatchText] = useState("");
  const [selectedModels, setSelectedModels] = useState(["claude-sonnet-4-6"]);
  const [results, setResults] = useState([]);
  const [batchResults, setBatchResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    const res = await axios.get(`${API_URL}/api/eval/history`);
    setHistory(res.data.history);
  };

  useEffect(() => { fetchHistory(); }, []);

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

  const runBatch = async () => {
    const prompts = batchText.split("\n").map(p => p.trim()).filter(Boolean);
    if (prompts.length === 0 || selectedModels.length === 0) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/api/eval/batch`, {
        prompts,
        models: selectedModels,
        task_type: "general",
      });
      setBatchResults(res.data.results);
      fetchHistory();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  // 단건 평가 차트 데이터: 모델별 지표 비교
  const chartData = results.map((r) => ({
    name: r.model_name.split("/").pop(),
    "LLM Judge": r.llm_score ?? r.score,
    "ROUGE-1": r.rouge1,
    "ROUGE-2": r.rouge2,
    "ROUGE-L": r.rougeL,
    "응답시간(초)": Math.round((r.latency_ms / 1000) * 10) / 10,
  }));

  // 배치 평가 요약: 모델별 평균 점수
  const batchSummary = (() => {
    const acc = {};
    batchResults.forEach(({ results: rs }) => {
      rs.forEach((r) => {
        if (!acc[r.model_name]) acc[r.model_name] = { count: 0, llm: 0, r1: 0, r2: 0, rL: 0 };
        acc[r.model_name].count++;
        acc[r.model_name].llm += r.llm_score ?? 0;
        acc[r.model_name].r1 += r.rouge1 ?? 0;
        acc[r.model_name].r2 += r.rouge2 ?? 0;
        acc[r.model_name].rL += r.rougeL ?? 0;
      });
    });
    return Object.entries(acc).map(([name, v]) => ({
      name: name.split("/").pop(),
      "LLM Judge (avg)": Math.round(v.llm / v.count * 100) / 100,
      "ROUGE-1 (avg)": Math.round(v.r1 / v.count * 1000) / 1000,
      "ROUGE-L (avg)": Math.round(v.rL / v.count * 1000) / 1000,
    }));
  })();

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2 text-purple-400">
          🧪 LLM Eval Pipeline
        </h1>
        <p className="text-center text-gray-500 mb-8 text-sm">
          Claude · GPT-4o Mini · Gemini — LLM Judge + ROUGE 복합 평가
        </p>

        {/* 탭 */}
        <div className="flex gap-2 mb-6">
          {["single", "batch"].map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-5 py-2 rounded-lg font-semibold text-sm transition ${
                tab === t ? "bg-purple-600 text-white" : "bg-gray-800 text-gray-400"
              }`}>
              {t === "single" ? "단건 평가" : "배치 평가"}
            </button>
          ))}
        </div>

        {/* 모델 선택 (공통) */}
        <div className="bg-gray-900 rounded-xl p-6 mb-6 shadow-lg">
          <p className="text-sm text-gray-400 mb-3">모델 선택</p>
          <div className="flex gap-3 flex-wrap">
            {MODELS.map((m) => (
              <button key={m.id} onClick={() => toggleModel(m.id)}
                className={`px-4 py-2 rounded-lg text-sm font-semibold border transition ${
                  selectedModels.includes(m.id)
                    ? "bg-purple-600 border-purple-500 text-white"
                    : "bg-gray-800 border-gray-600 text-gray-400"
                }`}>
                {m.label}
              </button>
            ))}
          </div>
        </div>

        {/* 단건 평가 */}
        {tab === "single" && (
          <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
            <textarea rows={4}
              className="w-full bg-gray-800 text-white rounded-lg p-4 text-base border border-gray-700 focus:outline-none focus:border-purple-500 resize-none"
              placeholder="평가할 프롬프트를 입력하세요..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button onClick={runEval} disabled={loading}
              className="w-full mt-4 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 text-white font-semibold rounded-lg transition">
              {loading ? "평가 중..." : "🚀 평가 실행"}
            </button>
          </div>
        )}

        {/* 배치 평가 */}
        {tab === "batch" && (
          <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
            <p className="text-sm text-gray-400 mb-2">프롬프트 목록 (줄바꿈으로 구분)</p>
            <textarea rows={8}
              className="w-full bg-gray-800 text-white rounded-lg p-4 text-base border border-gray-700 focus:outline-none focus:border-purple-500 resize-none font-mono text-sm"
              placeholder={"Python이란 무엇인가?\n머신러닝을 간단히 설명하라\nRAG의 장점은?"}
              value={batchText}
              onChange={(e) => setBatchText(e.target.value)}
            />
            <button onClick={runBatch} disabled={loading}
              className="w-full mt-4 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 text-white font-semibold rounded-lg transition">
              {loading ? "배치 평가 중..." : "🚀 배치 평가 실행"}
            </button>
          </div>
        )}

        {/* 단건 결과 */}
        {tab === "single" && results.length > 0 && (
          <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
            <h2 className="text-xl font-bold text-purple-400 mb-4">📊 평가 결과</h2>
            {results.map((r, i) => (
              <div key={i} className="bg-gray-800 rounded-lg p-4 mb-3">
                <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-2">
                  <span className="text-purple-400 font-semibold">{r.model_name}</span>
                  <span>LLM Judge: <b className="text-white">{r.llm_score ?? r.score}</b></span>
                  <span>ROUGE-1: <b className="text-cyan-400">{r.rouge1}</b></span>
                  <span>ROUGE-L: <b className="text-green-400">{r.rougeL}</b></span>
                  <span className="text-gray-500">{r.latency_ms}ms</span>
                </div>
                <p className="text-gray-200 text-sm leading-relaxed">{r.response}</p>
              </div>
            ))}
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-purple-400 mb-3">모델별 지표 비교</h3>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9ca3af" tick={{ fontSize: 12 }} />
                  <YAxis stroke="#9ca3af" domain={[0, 1]} />
                  <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
                  <Legend />
                  <Bar dataKey="LLM Judge" fill="#8b5cf6" />
                  <Bar dataKey="ROUGE-1" fill="#06b6d4" />
                  <Bar dataKey="ROUGE-L" fill="#10b981" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* 배치 결과 요약 */}
        {tab === "batch" && batchResults.length > 0 && (
          <div className="bg-gray-900 rounded-xl p-6 mb-8 shadow-lg">
            <h2 className="text-xl font-bold text-purple-400 mb-2">
              📦 배치 결과 — {batchResults.length}개 프롬프트
            </h2>
            {batchSummary.length > 0 && (
              <div className="mb-6">
                <h3 className="text-sm text-gray-400 mb-3">모델별 평균 점수</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={batchSummary}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="name" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" domain={[0, 1]} />
                    <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
                    <Legend />
                    <Bar dataKey="LLM Judge (avg)" fill="#8b5cf6" />
                    <Bar dataKey="ROUGE-1 (avg)" fill="#06b6d4" />
                    <Bar dataKey="ROUGE-L (avg)" fill="#10b981" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {batchResults.map((item, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-3">
                  <p className="text-xs text-gray-500 mb-2">#{i+1} {item.prompt.slice(0, 60)}...</p>
                  {item.results.map((r, j) => (
                    <div key={j} className="flex flex-wrap gap-3 text-xs text-gray-400 mb-1">
                      <span className="text-purple-300 font-semibold">{r.model_name.split("/").pop()}</span>
                      <span>Judge: <b className="text-white">{r.llm_score}</b></span>
                      <span>R1: <b className="text-cyan-400">{r.rouge1}</b></span>
                      <span>RL: <b className="text-green-400">{r.rougeL}</b></span>
                      <span className="text-gray-600">{r.latency_ms}ms</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 히스토리 */}
        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-purple-400 mb-4">📋 평가 히스토리</h2>
          {history.length === 0 && <p className="text-gray-500">히스토리가 없어요</p>}
          {history.map((h, i) => (
            <div key={i} className="bg-gray-800 rounded-lg p-4 mb-3">
              <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-1">
                <span className="text-purple-400 font-semibold">{h.model_name}</span>
                <span>Judge: <b className="text-white">{h.llm_score ?? h.score}</b></span>
                {h.rouge1 && <span>R1: <b className="text-cyan-400">{h.rouge1}</b></span>}
                {h.rougeL && <span>RL: <b className="text-green-400">{h.rougeL}</b></span>}
                <span className="text-gray-600 text-xs">{h.created_at}</span>
              </div>
              <p className="text-gray-300 text-sm">프롬프트: {h.prompt.slice(0, 80)}...</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;