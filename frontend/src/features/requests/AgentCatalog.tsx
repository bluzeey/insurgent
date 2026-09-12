import type { FlowKey } from './flowCopy';
import { flowCards } from './flowCopy';

export function AgentCatalog({ onSelectFlow }: { onSelectFlow: (flow: FlowKey) => void }) {
  return (
    <section className="agent-catalog" aria-labelledby="agents-title">
      <p className="eyebrow">My agents</p>
      <h1 id="agents-title">Create agents to collect insurance workflow data.</h1>
      <p className="intro">
        Pick the kind of data you need. The agent prepares a simple plan. You approve it before anything is sent.
      </p>
      <div className="agent-grid">
        {flowCards.map((agent) => (
          <article key={agent.flow} className="agent-card">
            <div>
              <p className="agent-label">{agent.label}</p>
              <h2>{agent.title}</h2>
              <p>{agent.description}</p>
            </div>
            <button className="button button-primary" type="button" onClick={() => onSelectFlow(agent.flow)}>
              Create agent
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
