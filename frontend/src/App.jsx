
import { useState } from "react";
import axios from "axios";
import {
  BarChart3,
  Database,
  Sparkles,
  Send,
  Loader2,
  AlertCircle,
  Code2,
  Table2,
  Lightbulb,
} from "lucide-react";

import "./App.css";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyzeQuestion = async () => {
    if (question.trim().length < 3 || loading) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        question: question.trim(),
      });

      const data = response.data;

      if (data.status !== "success") {
        throw new Error(data.error || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        "Unable to connect to the API."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><BarChart3 /></div>
          <span>InsightFlow</span>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <div className="nav-item active">
          <Sparkles size={18} />
          <span>AI Analyst</span>
        </div>

        <div className="nav-item">
          <Database size={18} />
          <span>Database</span>
        </div>

        <div className="sidebar-footer">
          <div className="status-dot" />
          API Connected
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <span>Workspace / AI Analyst</span>
          <span className="version">INSIGHTFLOW v1.0</span>
        </header>

        <section className="content">
          <div className="hero">
            <div className="eyebrow">
              <Sparkles size={15} /> AI-POWERED ANALYTICS
            </div>

            <h1>Business intelligence,<br />
              <span>simplified.</span>
            </h1>

            <p>
              Ask questions about your business data in plain English.
              Get SQL queries, analysis and actionable insights.
            </p>
          </div>

          <section className="query-card">
            <label htmlFor="question">ASK YOUR DATA</label>

            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  analyzeQuestion();
                }
              }}
              placeholder="e.g. Show top 5 products by delivered revenue in 2025"
              rows={3}
            />

            <div className="query-footer">
              <span>Press Enter to analyze</span>

              <button
                onClick={analyzeQuestion}
                disabled={loading || question.trim().length < 3}
              >
                {loading ? (
                  <><Loader2 className="spin" size={17} /> Analyzing</>
                ) : (
                  <><Send size={17} /> Analyze data</>
                )}
              </button>
            </div>
          </section>

          <div className="suggestions">
            <span>TRY ASKING</span>
            {[
              "Show top 5 products by revenue in 2025",
              "Show monthly revenue for 2025",
              "Compare revenue across years",
            ].map((item) => (
              <button key={item} onClick={() => setQuestion(item)}>
                {item}
              </button>
            ))}
          </div>

          {error && (
            <div className="error-box">
              <AlertCircle size={20} />
              <div>
                <strong>Analysis failed</strong>
                <p>{error}</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-box">
              <Loader2 className="spin" size={26} />
              <strong>Analyzing your data...</strong>
              <span>Generating SQL and processing business insights.</span>
            </div>
          )}

          {result && (
            <div className="results">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">ANALYSIS COMPLETE</span>
                  <h2>Your analysis</h2>
                </div>
                <span className="success-badge">Success</span>
              </div>

              <section className="result-card">
                <h3><Sparkles size={18} /> AI Business Insights</h3>
                <div className="answer markdown-answer">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {(result.answer || "").replace(/\\([*_#])/g, "$1")}
                  </ReactMarkdown>
                </div>
              </section>

              <section className="result-card">
                <h3><Table2 size={18} /> Query Results</h3>

                {result.results?.length > 0 ? (
                  <div className="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          {Object.keys(result.results[0]).map((key) => (
                            <th key={key}>{key.replaceAll("_", " ")}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {result.results.map((row, index) => (
                          <tr key={index}>
                            {Object.values(row).map((value, i) => (
                              <td key={i}>
                                {typeof value === "number"
                                  ? value.toLocaleString("en-IN", {
                                      maximumFractionDigits: 2,
                                    })
                                  : String(value ?? "-")}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p>No records returned.</p>
                )}
              </section>

              {result.calculations &&
                Object.keys(result.calculations).length > 0 && (
                  <section className="result-card">
                    <h3><Lightbulb size={18} /> Calculations</h3>
                    <pre>{JSON.stringify(result.calculations, null, 2)}</pre>
                  </section>
                )}

              
              {result.sql_query && (
                <details className="result-card sql-card">
                  <summary>
                    <Code2 size={18} /> Generated SQL
                  </summary>

                  <SyntaxHighlighter
                    language="sql"
                    style={vscDarkPlus}
                    showLineNumbers={true}
                    wrapLongLines={true}
                    customStyle={{
                      margin: 0,
                      borderRadius: "8px",
                      fontSize: "13px",
                      maxHeight: "450px",
                      overflow: "auto",
                      // whiteSpace: "pre-wrap",
                      // overflowWrap: "anywhere",
                    }}
                  >
                    {result.sql_query
                      .replace(/\bSELECT\b/gi, "\nSELECT")
                      .replace(/\bFROM\b/gi, "\nFROM")
                      .replace(/\bJOIN\b/gi, "\nJOIN")
                      .replace(/\bLEFT JOIN\b/gi, "\nLEFT JOIN")
                      .replace(/\bWHERE\b/gi, "\nWHERE")
                      .replace(/\bGROUP BY\b/gi, "\nGROUP BY")
                      .replace(/\bORDER BY\b/gi, "\nORDER BY")
                      .replace(/\bHAVING\b/gi, "\nHAVING")
                      .replace(/\bLIMIT\b/gi, "\nLIMIT")
                      .trim()}
                  </SyntaxHighlighter>
                </details>
              )}

              {result.chart_required && result.chart_path && (
                <div className="result-card chart-card">
                  <h3>Data Visualization</h3>

                  <iframe
                    src={`${API_URL}/charts/${result.chart_path.split(/[\\/]/).pop()}`}
                    title="Generated Data Chart"
                    className="chart-frame"
                  />
                </div>
              )}
              {result.chart_path && (
                <p className="chart-note">
                  Chart generated: {result.chart_type}
                  <br />
                  The chart file is saved on the backend.
                </p>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
