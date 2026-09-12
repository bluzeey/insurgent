import { Button } from '../../components/Button';
import { StatusPill } from '../../components/StatusPill';
import type { InformationRequest } from '../../lib/api/types';

export function RequestDetail({
  item,
  onApprove,
  onCancel,
  onClosePartial,
  busy,
}: {
  item?: InformationRequest;
  onApprove: (item: InformationRequest) => Promise<void>;
  onCancel: (item: InformationRequest) => Promise<void>;
  onClosePartial: (item: InformationRequest) => Promise<void>;
  busy: boolean;
}) {
  if (!item) {
    return (
      <section className="detail empty-state">
        <p className="eyebrow">Agent run</p>
        <h2>Create your first data collection agent.</h2>
        <p>If the agent cannot find an approved contact or safe scope, it stops and asks you to clarify.</p>
      </section>
    );
  }

  const plan = item.activePlan;
  const result = item.result;

  return (
    <section className="detail" aria-label="Request detail">
      <div className="detail-header">
        <div>
          <p className="eyebrow">Agent run {item.id}</p>
          <h2>{plan?.objective ?? item.instruction}</h2>
        </div>
        <StatusPill status={item.status} />
      </div>

      {plan ? (
        <div className="panel">
          <h3>Agent plan</h3>
          {plan.blockingClarifications.length ? (
            <div className="warning">
              <strong>Needs clarification</strong>
              <ul>
                {plan.blockingClarifications.map((text) => (
                  <li key={text}>{text}</li>
                ))}
              </ul>
            </div>
          ) : null}
          <dl className="plan-grid">
            <div>
              <dt>Who</dt>
              <dd>{plan.respondent ? `${plan.respondent.name}, ${plan.respondent.organization} · ${plan.respondent.email}` : 'Not resolved'}</dd>
            </div>
            <div>
              <dt>Method</dt>
              <dd>
                {plan.method.channel}; {plan.method.reminderCount} reminder after {plan.method.reminderAfterHours}h
              </dd>
            </div>
            <div>
              <dt>Limits</dt>
              <dd>
                Deadline {new Date(plan.limits.deadline).toLocaleString()} · max {plan.limits.maxTouches} touches
                {plan.limits.forbiddenChannels.length ? ` · forbidden: ${plan.limits.forbiddenChannels.join(', ')}` : ''}
              </dd>
            </div>
            <div>
              <dt>Deliver</dt>
              <dd>{plan.deliverable}</dd>
            </div>
          </dl>
          <h4>Collect</h4>
          <ul className="questions">
            {plan.questions.map((question) => (
              <li key={question.id}>
                <span>{question.label}</span>
                <small>{question.required ? 'Required' : 'Optional'} · {question.evidenceRule}</small>
              </li>
            ))}
          </ul>
          {plan.alreadyAvailable.length ? (
            <p className="muted">Already available: {plan.alreadyAvailable.join('; ')}</p>
          ) : null}
          <div className="action-row">
            {item.allowedActions.includes('approve') ? (
              <Button variant="primary" onClick={() => onApprove(item)} disabled={busy}>
                Approve agent plan
              </Button>
            ) : null}
            {item.allowedActions.includes('cancel') ? (
              <Button onClick={() => onCancel(item)} disabled={busy}>Cancel</Button>
            ) : null}
          </div>
        </div>
      ) : null}

      {result ? (
        <div className="panel">
          <h3>Collected data</h3>
          <p>{result.summary}</p>
          <div className="answers">
            {result.answers.map((answer) => (
              <article key={answer.questionId} className="answer-card">
                <strong>{answer.question}</strong>
                <p>{answer.rawValue ?? 'Unresolved'}</p>
                <small>{answer.status}{answer.source ? ` · ${answer.source}` : ''}</small>
              </article>
            ))}
          </div>
          {result.unresolvedItems.length ? (
            <div className="warning">
              <strong>Remaining gaps</strong>
              <ul>
                {result.unresolvedItems.map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          ) : null}
          {item.allowedActions.includes('close_partial') ? (
            <div className="action-row">
              <Button variant="primary" onClick={() => onClosePartial(item)} disabled={busy}>Close with gaps</Button>
            </div>
          ) : null}
        </div>
      ) : null}

      <details className="events">
        <summary>Activity and sources</summary>
        <ol>
          {item.events.map((event) => (
            <li key={event.sequence}>
              <strong>{event.type}</strong> — {event.message}
            </li>
          ))}
        </ol>
      </details>
    </section>
  );
}
