import { useState } from "react";

const CATEGORY_META = {
  bug:         { label: "Bug",         icon: "🐛", color: "#f85149", bg: "rgba(248,81,73,0.1)",  border: "rgba(248,81,73,0.25)"  },
  performance: { label: "Performance", icon: "⚡", color: "#d29922", bg: "rgba(210,153,34,0.1)", border: "rgba(210,153,34,0.25)" },
  style:       { label: "Style",       icon: "✏️",  color: "#58a6ff", bg: "rgba(88,166,255,0.1)", border: "rgba(88,166,255,0.25)" },
  security:    { label: "Security",    icon: "🔒", color: "#bc8cff", bg: "rgba(188,140,255,0.1)",border: "rgba(188,140,255,0.25)"},
};

const SEVERITY_META = {
  critical: { label: "Critical", color: "#f85149", border: "rgba(248,81,73,0.4)"  },
  high:     { label: "High",     color: "#d29922", border: "rgba(210,153,34,0.4)" },
  medium:   { label: "Medium",   color: "#58a6ff", border: "rgba(88,166,255,0.4)" },
  low:      { label: "Low",      color: "#8b949e", border: "rgba(139,148,158,0.3)"},
};

export default function ReviewCard({ issue, index }) {
  const [expanded, setExpanded] = useState(true);

  const cat = CATEGORY_META[issue.category] || CATEGORY_META.style;
  const sev = SEVERITY_META[issue.severity] || SEVERITY_META.low;

  return (
    <div
      className="review-card"
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      {/* Header */}
      <div className="card-header" onClick={() => setExpanded((v) => !v)}>
        <div className="card-left">
          <span
            className="cat-badge"
            style={{ background: cat.bg, color: cat.color, borderColor: cat.border }}
          >
            {cat.icon} {cat.label}
          </span>
          <span
            className="sev-badge"
            style={{ color: sev.color, borderColor: sev.border }}
          >
            {sev.label}
          </span>
          <span className="card-title">{issue.title}</span>
        </div>
        <div className="card-meta">
          <code className="file-chip">{issue.file}:{issue.line}</code>
          <span className="expand-icon">{expanded ? "▲" : "▼"}</span>
        </div>
      </div>

      {/* Body */}
      {expanded && (
        <div className="card-body">
          <div className="card-section">
            <div className="section-label">Problem</div>
            <p className="section-text">{issue.description}</p>
          </div>
          <div className="card-section suggestion-section">
            <div className="section-label suggestion-label">Suggestion</div>
            <p className="section-text">{issue.suggestion}</p>
          </div>
        </div>
      )}
    </div>
  );
}