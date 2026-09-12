const agents = [
  {
    title: 'Form collection agent',
    text: 'Collect basic form data from an approved contact.',
  },
  {
    title: 'Clarification agent',
    text: 'Ask for missing numbers, dates, units, or documents.',
  },
  {
    title: 'Renewal changes agent',
    text: 'Check what changed since last year.',
  },
];

const steps = [
  'Choose an agent',
  'Review the plan',
  'Approve the run',
  'Get the collected data',
];

export function LandingPage() {
  return (
    <main className="landing-page">
      <header className="landing-nav">
        <a className="wordmark" href="/">Insurgent</a>
        <nav aria-label="Primary navigation">
          <a href="#agents">Agents</a>
          <a href="#how">How it works</a>
          <a href="/dashboard">Open dashboard</a>
        </nav>
      </header>

      <section className="landing-hero">
        <p className="eyebrow">Insurance workflow data</p>
        <h1>
          Create agents.<br />
          <em>Collect the data.</em>
        </h1>
        <p className="hero-copy">
          Insurgent helps insurance teams create simple agents that collect data for their workflows. Start with a form collection agent, review the plan, and approve the run.
        </p>
        <div className="hero-actions">
          <a className="button button-primary" href="/dashboard">Create an agent</a>
          <a className="text-link" href="#agents">See agent types</a>
        </div>
        <p className="notice-line">This is a dry run. No real emails or calls are sent.</p>
      </section>

      <section className="landing-section" id="agents">
        <p className="eyebrow">Agent types</p>
        <h2>Start with the data you need.</h2>
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
          <h2>The app stays simple.</h2>
        </div>
        <ul className="safeguard-list">
          {steps.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </section>

      <section className="landing-section split">
        <div>
          <p className="eyebrow">Controls</p>
          <h2>You stay in control.</h2>
        </div>
        <div className="section-copy">
          <p>No agent contacts anyone before you approve the plan.</p>
          <p>If the contact or scope is unclear, the agent stops and asks you to clarify.</p>
          <p>Every result shows what was answered, what is still missing, and where the answer came from.</p>
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
