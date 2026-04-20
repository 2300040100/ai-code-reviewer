const SEVERITY_META = {
  critical: { label: "Critical", color: "#f85149", bg: "rgba(248,81,73,0.08)",   border: "rgba(248,81,73,0.25)"   },
  high:     { label: "High",     color: "#d29922", bg: "rgba(210,153,34,0.08)",  border: "rgba(210,153,34,0.25)"  },
  medium:   { label: "Medium",   color: "#58a6ff", bg: "rgba(88,166,255,0.08)",  border: "rgba(88,166,255,0.25)"  },
  low:      { label: "Low",      color: "#8b949e", bg: "rgba(139,148,158,0.08)", border: "rgba(139,148,158,0.2)"  },
};

export default function SummaryBar({ summary, stats = {}, prTitle, prUrl, onCopyReport }) {
  return (
    <div className="summary-bar">

      {/* Header row */}
      <div className="summary-header">
        <div className="summary-title-group">
          <div className="summary-pr-title">{prTitle}</div>
          <a href={prUrl} target="_blank" rel="noreferrer" className="summary-pr-url">
            {prUrl}
          </a>
        </div>
        <button className="copy-btn" onClick={onCopyReport}>
          📋 Copy as Markdown
        </button>
      </div>

      {/* PR stats — only show if stats exist */}
      {stats.author && (
        <div className="stats-row">
          <div className="stat-chip">
            <span>👤</span>
            <span className="stat-text">{stats.author}</span>
          </div>
          <div className="stat-chip">
            <span>📂</span>
            <span className="stat-text">{stats.files_reviewed} files reviewed</span>
          </div>
          <div className="stat-chip">
            <span style={{ color: "#3fb950", fontWeight: 700 }}>
              +{stats.total_additions}
            </span>
          </div>
          <div className="stat-chip">
            <span style={{ color: "#f85149", fontWeight: 700 }}>
              −{stats.total_deletions}
            </span>
          </div>
          <div className="stat-chip">
            <span>🌿</span>
            <span className="stat-text">
              {stats.base_branch} ← {stats.head_branch}
            </span>
          </div>
        </div>
      )}

      {/* Severity chips */}
      <div className="severity-chips">
        {Object.entries(SEVERITY_META).map(([key, meta]) => (
          <div
            key={key}
            className="severity-chip"
            style={{
              background: meta.bg,
              color: meta.color,
              borderColor: meta.border,
            }}
          >
            <span className="chip-count">{summary[key]}</span>
            <span className="chip-label">{meta.label}</span>
          </div>
        ))}
      </div>

      {/* Overall assessment */}
      <div className="assessment-box">
        <span className="assessment-label">Overall Assessment</span>
        <p className="assessment-text">{summary.overall_assessment}</p>
      </div>

    </div>
  );
}