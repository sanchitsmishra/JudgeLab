import type { EvaluationReport, SavedSessionSummary } from "../types/evaluation";
import { Activity, ArrowUpRight, BarChart3, CheckCircle2, Clock3 } from "lucide-react";

interface AnalyticsOverviewProps {
  sessions: SavedSessionSummary[];
  report: EvaluationReport | null;
  onStartEvaluation: () => void;
}

export const AnalyticsOverview = ({ sessions, report, onStartEvaluation }: AnalyticsOverviewProps) => {
  const rankings = report?.rankings ?? [];
  const averageScore = rankings.length
    ? Math.round(rankings.reduce((sum, item) => sum + item.average_correctness, 0) / rankings.length)
    : 0;
  const totalComparisons = report?.metrics.evaluation?.total_comparisons ?? 0;
  const recent = sessions.slice(0, 4);

  return (
    <section className="overview-page">
      <div className="overview-hero">
        <div>
          <span className="eyebrow"><Activity size={14} /> Evaluation workspace</span>
          <h1>Make every model decision measurable.</h1>
          <p>Run side-by-side evaluations, inspect judge outcomes, and keep your AI stack accountable.</p>
        </div>
        <button className="btn-primary" onClick={onStartEvaluation}><ArrowUpRight size={17} /> New evaluation</button>
      </div>

      <div className="analytics-grid stats-grid">
        <article className="metric-card"><span>Saved evaluations</span><strong>{sessions.length}</strong><small><CheckCircle2 size={14} /> Available in your history</small></article>
        <article className="metric-card"><span>Models ranked</span><strong>{rankings.length || "—"}</strong><small><BarChart3 size={14} /> Current evaluation</small></article>
        <article className="metric-card"><span>Avg. correctness</span><strong>{rankings.length ? `${averageScore}%` : "—"}</strong><small><Activity size={14} /> Judge-reported score</small></article>
        <article className="metric-card"><span>Comparisons run</span><strong>{totalComparisons || "—"}</strong><small><Clock3 size={14} /> Current evaluation</small></article>
      </div>

      <div className="analytics-grid overview-lower-grid">
        <article className="dashboard-card performance-card">
          <div className="card-title"><div><span className="eyebrow">Live report</span><h2>Model performance</h2></div><BarChart3 size={19} /></div>
          {rankings.length ? rankings.slice(0, 5).map((item) => (
            <div className="ranking-row" key={item.model_id}>
              <span className="rank-number">{item.rank}</span><span className="ranking-name">{item.model_name}</span>
              <div className="score-track"><i style={{ width: `${Math.min(100, Math.max(0, item.win_rate * 100))}%` }} /></div>
              <strong>{Math.round(item.win_rate * 100)}%</strong>
            </div>
          )) : <div className="empty-insight">Your next evaluation will populate performance analytics here.</div>}
        </article>
        <article className="dashboard-card activity-card">
          <div className="card-title"><div><span className="eyebrow">Activity</span><h2>Recent evaluations</h2></div></div>
          {recent.length ? recent.map((session) => <div className="activity-row" key={session.session_id}><span className="activity-dot" /><div><strong>{session.models.join(" · ") || "Evaluation"}</strong><small>{session.prompt_preview || session.mode}</small></div><em>{session.status.replaceAll("_", " ")}</em></div>) : <div className="empty-insight">Saved evaluations will appear here.</div>}
        </article>
      </div>
    </section>
  );
};
