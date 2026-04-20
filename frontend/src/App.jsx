import { useState, useEffect } from "react";
import PRInput from "./components/PRInput";
import SummaryBar from "./components/SummaryBar";
import ReviewCard from "./components/ReviewCard";
import { reviewPR } from "./services/api";
import "./App.css";

const CATEGORY_ORDER = ["bug", "performance", "security", "style"];
const SEVERITY_ORDER = ["critical", "high", "medium", "low"];

const LOADING_STEPS = [
  { icon: "🔗", text: "Connecting to GitHub" },
  { icon: "📂", text: "Fetching PR files" },
  { icon: "🧠", text: "Reading the code" },
  { icon: "🔍", text: "Analyzing issues" },
  { icon: "📝", text: "Building report" },
];

export default function App() {
  const [loading, setLoading]               = useState(false);
  const [loadingStep, setLoadingStep]       = useState(0);
  const [result, setResult]                 = useState(null);
  const [error, setError]                   = useState(null);
  const [activeCategory, setActiveCategory] = useState("all");
  const [activeSeverity, setActiveSeverity] = useState("all");
  const [lightMode, setLightMode]           = useState(false);

  useEffect(() => {
    if (!loading) { setLoadingStep(0); return; }
    const iv = setInterval(() => {
      setLoadingStep((p) => (p < LOADING_STEPS.length - 1 ? p + 1 : p));
    }, 5000);
    return () => clearInterval(iv);
  }, [loading]);

  useEffect(() => {
    document.body.classList.toggle("light", lightMode);
  }, [lightMode]);

  const handleSubmit = async (prUrl, focusAreas) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setActiveCategory("all");
    setActiveSeverity("all");
    try {
      const data = await reviewPR(prUrl, focusAreas);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyReport = () => {
    if (!result) return;
    const lines = [
      `# AI Code Review — ${result.pr_title}`,
      `**PR:** ${result.pr_url}`,
      `**Author:** ${result.stats.author}`,
      `**Files reviewed:** ${result.stats.files_reviewed}`,
      `**Total issues:** ${result.summary.total_issues}`,
      "",
      `## Overall Assessment`,
      result.summary.overall_assessment,
      "",
      `## Issues`,
    ];
    result.issues.forEach((issue, i) => {
      lines.push(
        `### ${i + 1}. [${issue.severity.toUpperCase()}] ${issue.title}`,
        `- **Category:** ${issue.category}`,
        `- **File:** \`${issue.file}\` (line ${issue.line})`,
        `- **Problem:** ${issue.description}`,
        `- **Suggestion:** ${issue.suggestion}`,
        ""
      );
    });
    navigator.clipboard.writeText(lines.join("\n"));
    alert("✅ Review copied to clipboard as Markdown!");
  };

  const filteredIssues = result
    ? result.issues.filter((i) => {
        const c = activeCategory === "all" || i.category === activeCategory;
        const s = activeSeverity === "all" || i.severity === activeSeverity;
        return c && s;
      })
    : [];

  const sevOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  const sortedIssues = [...filteredIssues].sort(
    (a, b) => (sevOrder[a.severity] ?? 4) - (sevOrder[b.severity] ?? 4)
  );

  return (
    <div className="app">

      {/* ── Header ── */}
      <div className="app-header">
        <div className="header-left">
          <div className="header-logo-wrap">🔍</div>
          <div>
            <div className="header-title">
              AI Code Reviewer
              <span className="header-badge" style={{ marginLeft: "0.5rem" }}>Beta</span>
            </div>
            <div className="header-sub">Powered by Groq AI · GitHub API</div>
          </div>
        </div>
        <button className="dark-toggle" onClick={() => setLightMode((v) => !v)}>
          {lightMode ? "🌙 Dark" : "☀️ Light"}
        </button>
      </div>

      {/* ── Input ── */}
      <PRInput
        onSubmit={handleSubmit}
        loading={loading}
        loadingStep={loadingStep}
        loadingSteps={LOADING_STEPS}
      />

      {/* ── Error ── */}
      {error && (
        <div className="error-box">
          <div className="error-icon">⚠️</div>
          <div className="error-body">
            <div className="error-title">Something went wrong</div>
            <div className="error-detail">{error}</div>
            <div className="error-hint">
              💡 Make sure the PR URL is correct and the repository is public.
            </div>
          </div>
        </div>
      )}

      {/* ── Results ── */}
      {result && (
        <>
          <SummaryBar
            summary={result.summary}
            stats={result.stats}
            prTitle={result.pr_title}
            prUrl={result.pr_url}
            onCopyReport={copyReport}
          />

          {/* Category filter */}
          <div className="filter-section">
            <div className="filter-label">Filter by Category</div>
            <div className="filter-bar">
              {["all", ...CATEGORY_ORDER].map((cat) => {
                const count = cat === "all"
                  ? result.issues.length
                  : result.issues.filter((i) => i.category === cat).length;
                return (
                  <button
                    key={cat}
                    className={`filter-tab ${activeCategory === cat ? "active" : ""}`}
                    onClick={() => setActiveCategory(cat)}
                  >
                    {cat === "all" ? "All" : cat.charAt(0).toUpperCase() + cat.slice(1)}
                    <span className="tab-count">{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Severity filter */}
          <div className="filter-section">
            <div className="filter-label">Filter by Severity</div>
            <div className="filter-bar">
              {["all", ...SEVERITY_ORDER].map((sev) => {
                const count = sev === "all"
                  ? result.issues.length
                  : result.issues.filter((i) => i.severity === sev).length;
                return (
                  <button
                    key={sev}
                    className={`filter-tab sev-tab sev-${sev} ${activeSeverity === sev ? "active" : ""}`}
                    onClick={() => setActiveSeverity(sev)}
                  >
                    {sev === "all" ? "All" : sev.charAt(0).toUpperCase() + sev.slice(1)}
                    <span className="tab-count">{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Issues */}
          <div className="issues-list">
            {sortedIssues.length === 0 ? (
              <div className="no-issues">
                <div className="no-issues-icon">🎉</div>
                <div className="no-issues-text">No issues in this filter</div>
                <div className="no-issues-sub">Try a different category or severity</div>
              </div>
            ) : (
              sortedIssues.map((issue, i) => (
                <ReviewCard key={i} issue={issue} index={i} />
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}