import { useState } from "react";

const FOCUS_OPTIONS = [
  { id: "bugs",        label: "🐛  Bug Detection",              color: "#f85149" },
  { id: "performance", label: "⚡  Performance Issues",          color: "#d29922" },
  { id: "style",       label: "✏️   Code Style",                 color: "#58a6ff" },
  { id: "security",    label: "🔒  Security Vulnerabilities",    color: "#bc8cff" },
];

export default function PRInput({ onSubmit, loading, loadingStep, loadingSteps }) {
  const [prUrl, setPrUrl]         = useState("");
  const [focusAreas, setFocusAreas] = useState(["bugs","performance","style","security"]);

  const toggleFocus = (id) =>
    setFocusAreas((prev) =>
      prev.includes(id) ? prev.filter((f) => f !== id) : [...prev, id]
    );

  const handleSubmit = () => {
    if (!prUrl.trim() || focusAreas.length === 0) return;
    onSubmit(prUrl.trim(), focusAreas);
  };

  return (
    <div className="input-card">
      <label className="field-label">GitHub PR URL</label>
      <input
        className="pr-input"
        type="url"
        placeholder="https://github.com/owner/repo/pull/123"
        value={prUrl}
        onChange={(e) => setPrUrl(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        disabled={loading}
      />

      <label className="field-label" style={{ marginTop: "1.25rem" }}>
        Focus Areas
      </label>
      <div className="focus-grid">
        {FOCUS_OPTIONS.map((opt) => {
          const active = focusAreas.includes(opt.id);
          return (
            <button
              key={opt.id}
              className={`focus-chip ${active ? "active" : ""}`}
              style={active ? {
                borderColor: opt.color,
                color: opt.color,
                background: opt.color + "10",
              } : {}}
              onClick={() => toggleFocus(opt.id)}
              disabled={loading}
            >
              {opt.label}
            </button>
          );
        })}
      </div>

      <button
        className="review-btn"
        onClick={handleSubmit}
        disabled={loading || !prUrl.trim() || focusAreas.length === 0}
      >
        {loading ? (
          <span className="btn-loading">
            <span className="spinner" />
            {loadingSteps[loadingStep]?.icon} {loadingSteps[loadingStep]?.text}...
          </span>
        ) : (
          "→ Run AI Review"
        )}
      </button>

      {loading && (
        <>
          <div className="loading-bar-wrap">
            <div className="loading-bar" />
          </div>
          <div className="loading-steps">
            {loadingSteps.map((step, i) => (
              <div
                key={i}
                className={`loading-step ${i === loadingStep ? "active" : ""}`}
              >
                <span>{step.icon}</span>
                <span>{step.text}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}