import React from "react";
import ReactDOM from "react-dom/client";
import { BookOpen, BrainCircuit, GraduationCap, Loader2, Send, Sparkles } from "lucide-react";

import "./styles.css";

type Citation = {
  chunk_id: string;
  page: number | null;
  chapter: string | null;
  section: string | null;
  text: string;
  score: number | null;
};

type AskResponse = {
  answer: string;
  citations: Citation[];
  grounded: boolean;
};

const modeOptions = [
  { id: "classroom", label: "课堂解释", icon: GraduationCap },
  { id: "review", label: "复习重点", icon: BrainCircuit },
  { id: "homework_hint", label: "作业提示", icon: Sparkles }
];

function App() {
  const [question, setQuestion] = React.useState("冰冻圈包括哪些组成部分？它为什么对气候系统很重要？");
  const [mode, setMode] = React.useState("classroom");
  const [loading, setLoading] = React.useState(false);
  const [response, setResponse] = React.useState<AskResponse | null>(null);
  const [error, setError] = React.useState("");

  async function ask() {
    const trimmed = question.trim();
    if (!trimmed) return;

    setLoading(true);
    setError("");
    try {
      const result = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed, mode, top_k: 5 })
      });
      if (!result.ok) {
        throw new Error(`请求失败：${result.status}`);
      }
      setResponse(await result.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "请求失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <BookOpen size={24} />
          <div>
            <h1>冰冻圈科学课堂助教智能体</h1>
            <p>DeepSeek V4 + 权威教材的课堂辅助教学</p>
          </div>
        </div>

        <nav className="nav-list">
          <button className="nav-item active">教材问答</button>
          <button className="nav-item">章节学习</button>
          <button className="nav-item">概念复习</button>
          <button className="nav-item">课堂小测</button>
        </nav>

        <section className="status-panel">
          <span>当前知识源</span>
          <strong>《冰冻圈科学概论》</strong>
          <p>回答会优先检索教材片段，并展示引用来源。</p>
        </section>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">学生端 MVP</span>
            <h2>基于教材出处的课堂问答</h2>
          </div>
          <div className="mode-switch" aria-label="回答模式">
            {modeOptions.map((option) => {
              const Icon = option.icon;
              return (
                <button
                  key={option.id}
                  className={mode === option.id ? "mode-button active" : "mode-button"}
                  onClick={() => setMode(option.id)}
                  title={option.label}
                >
                  <Icon size={17} />
                  <span>{option.label}</span>
                </button>
              );
            })}
          </div>
        </header>

        <section className="ask-panel">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="输入你想理解的冰冻圈科学问题..."
          />
          <button className="send-button" onClick={ask} disabled={loading}>
            {loading ? <Loader2 className="spin" size={18} /> : <Send size={18} />}
            <span>{loading ? "检索教材中" : "提问"}</span>
          </button>
        </section>

        {error && <div className="error">{error}</div>}

        <section className="answer-grid">
          <article className="answer-panel">
            <h3>助教回答</h3>
            <div className="answer-body">
              {response ? response.answer : "提问后，这里会显示基于教材检索生成的回答。"}
            </div>
          </article>

          <article className="citation-panel">
            <h3>教材依据</h3>
            <div className="citation-list">
              {response?.citations.length ? (
                response.citations.map((citation) => (
                  <div className="citation-card" key={citation.chunk_id}>
                    <div className="citation-meta">
                      <span>第 {citation.page ?? "?"} 页</span>
                      <span>{citation.score ? `相关度 ${citation.score}` : "已召回"}</span>
                    </div>
                    {citation.chapter && <strong>{citation.chapter}</strong>}
                    <p>{citation.text}</p>
                  </div>
                ))
              ) : (
                <p className="muted">暂无引用。建立教材知识库并提问后，会显示召回片段。</p>
              )}
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
