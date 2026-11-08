import React from "react";
import { ArrowRight, Check, Scale, Sparkles } from "lucide-react";
import { ThemeToggle, type AppTheme } from "./ThemeToggle";
import heroImage from "../assets/llm-judge-welcome.png";
import "./WelcomePage.css";

interface WelcomePageProps {
  onNext: () => void;
  onSignIn: () => void;
  theme: AppTheme;
  onToggleTheme: () => void;
}

export const WelcomePage: React.FC<WelcomePageProps> = ({ onNext, onSignIn, theme, onToggleTheme }) => (
  <main className="welcome-shell">
    <header className="welcome-header">
      <a className="welcome-brand" href="#welcome" aria-label="JudgeLab home">
        <span className="welcome-brand-icon"><Scale size={21} aria-hidden="true" /></span>
        <span>JudgeLab</span>
        <span className="welcome-brand-badge">Evaluation intelligence</span>
      </a>
      <div className="welcome-header-actions">
        <span className="welcome-header-note"><Sparkles size={15} aria-hidden="true" /> Evidence-led model decisions</span>
        <ThemeToggle theme={theme} onToggle={onToggleTheme} />
      </div>
    </header>

    <section className="welcome-layout" id="welcome">
      <div className="welcome-copy">
        <div className="welcome-eyebrow"><span /> AI evaluation, made measurable</div>
        <h1>Evaluate smarter. <span>Trust better.</span></h1>
        <p className="welcome-description">
          JudgeLab brings model responses into one focused workspace, so your team can compare outcomes, review evidence, and move forward with confidence.
        </p>

        <div className="welcome-workflow" aria-label="How JudgeLab works">
          <div className="welcome-workflow-step">
            <span className="welcome-step-number">01</span>
            <span className="welcome-step-text"><strong>Bring a question</strong><small>Use your prompt or answers</small></span>
          </div>
          <span className="welcome-step-line" aria-hidden="true" />
          <div className="welcome-workflow-step">
            <span className="welcome-step-number">02</span>
            <span className="welcome-step-text"><strong>Evaluate</strong><small>Review every response clearly</small></span>
          </div>
          <span className="welcome-step-line" aria-hidden="true" />
          <div className="welcome-workflow-step">
            <span className="welcome-step-number">03</span>
            <span className="welcome-step-text"><strong>Choose</strong><small>See results and decide</small></span>
          </div>
        </div>

        <div className="welcome-actions">
          <button className="welcome-next-button" onClick={onNext}>
            <span>Next</span><ArrowRight size={18} aria-hidden="true" />
          </button>
          <p>Already have an account? <button className="welcome-signin-link" onClick={onSignIn}>Sign in</button></p>
        </div>

        <div className="welcome-points">
          <span><Check size={15} aria-hidden="true" /> Answers side by side</span>
          <span><Check size={15} aria-hidden="true" /> Results you can review</span>
          <span><Check size={15} aria-hidden="true" /> Your own model providers</span>
        </div>
      </div>

      <figure className="welcome-visual">
        <img src={heroImage} alt="Researchers comparing AI model evaluation results on a screen" />
        <div className="welcome-visual-wash" aria-hidden="true" />
        <figcaption className="welcome-image-caption">
          <span className="welcome-caption-icon"><Sparkles size={17} aria-hidden="true" /></span>
          <span><strong>Clarity for every decision</strong><small>Compare the evidence, then make the call.</small></span>
        </figcaption>
        <div className="welcome-score-card" aria-hidden="true">
          <span className="welcome-score-label">PAIRWISE RESULT</span>
          <span className="welcome-score-title">Answer A leads</span>
          <span className="welcome-score-bars"><i /><i /></span>
          <span className="welcome-score-foot"><span>Correctness</span><b>Evaluated</b></span>
        </div>
      </figure>
    </section>

    <footer className="welcome-footer">
      <span>For teams building dependable AI systems</span>
      <span><span className="welcome-footer-dot" /> Structured pairwise evaluation</span>
    </footer>
  </main>
);
