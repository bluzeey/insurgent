const agents = [
  {
    title: 'Form collection agent',
    text: 'Turns an approved checklist or form into a focused collection run.',
  },
  {
    title: 'Clarification agent',
    text: 'Follows up on missing numbers, dates, units, documents, and source evidence.',
  },
  {
    title: 'Renewal changes agent',
    text: 'Asks what changed since last year without assuming old facts are still true.',
  },
];

const steps = [
  'Describe the gap in plain English.',
  'Insuveo resolves the contact, questions, limits, and delivery format.',
  'You review the exact plan before anything is sent.',
  'The agent collects, follows up, stops on ambiguity, and returns sourced answers.',
];

export function LandingPage() {
  return (
    <main className="landing-page">
      <header className="landing-nav">
        <a className="wordmark" href="/">insuveo</a>
        <nav aria-label="Primary navigation">
          <a href="#product">Product</a>
          <a href="#agents">Agents</a>
          <a href="#how">How it works</a>
          <a href="/dashboard">Open dashboard</a>
        </nav>
      </header>

      <section className="landing-hero" id="product">
        <p className="eyebrow">AI agents for insurance workflow data</p>
        <h1>
          One instruction replaces the chase.<br />
          <em>Insuveo runs the follow-up.</em>
        </h1>
        <p className="hero-copy">
          Insuveo turns a plain-English request into a bounded data-collection agent. It finds the approved contact, asks only for the missing facts, follows up inside your limits, and returns a source-linked summary.
        </p>
        <div className="hero-actions">
          <a className="button button-primary" href="/dashboard">Create an agent</a>
          <a className="text-link" href="#how">See how it works</a>
        </div>
        <p className="notice-line">Dry run mode: no real emails or calls are sent.</p>
      </section>

      <section className="landing-section" id="agents">
        <p className="eyebrow">Today</p>
        <h2>Agents that run insurance information operations.</h2>
        <div className="workflow-grid">
          {agents.map((item) => (
            <article key={item.title} className="landing-card">
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section split" id="how">
        <div>
          <p className="eyebrow">How it works</p>
          <h2>The agent does the mechanical work. You keep the judgment.</h2>
        </div>
        <ul className="safeguard-list">
          {steps.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </section>

      <section className="landing-section split">
        <div>
          <p className="eyebrow">Platform</p>
          <h2>Your team and the agents share the same request record.</h2>
        </div>
        <div className="section-copy">
          <p>Each agent run has a plan, approval, status, next action, collected answers, gaps, and sources.</p>
          <p>No agent contacts anyone before approval. If the contact or scope is unclear, it stops and asks you to clarify.</p>
          <p>The goal is not autonomous insurance judgment. Insuveo handles the chase so insurance teams can review facts, make decisions, and work with clients.</p>
        </div>
      </section>

      <section className="landing-cta">
        <h2>Create your first agent.</h2>
        <p>Open the dashboard and choose Form collection agent.</p>
        <a className="button button-primary" href="/dashboard">Open dashboard</a>
      </section>
    </main>
  );
}
