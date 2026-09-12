import { useEffect, useState } from 'react';
import { Button } from '../../components/Button';
import type { FlowKey } from './flowCopy';
import { getFlowCard } from './flowCopy';

export function Composer({
  flow,
  onSubmit,
  busy,
}: {
  flow: FlowKey;
  onSubmit: (instruction: string) => Promise<void>;
  busy: boolean;
}) {
  const activeFlow = getFlowCard(flow);
  const [instruction, setInstruction] = useState(activeFlow.example);

  useEffect(() => {
    setInstruction(activeFlow.example);
  }, [activeFlow.example]);

  async function submit() {
    if (instruction.trim().length < 8) return;
    await onSubmit(instruction.trim());
  }

  return (
    <section className="composer-card" aria-labelledby="composer-title">
      <div>
        <p className="eyebrow">Create agent</p>
        <h1 id="composer-title">{activeFlow.title}</h1>
        <p className="intro">{activeFlow.description} Edit the instruction, then create a dry run plan.</p>
      </div>
      <textarea
        value={instruction}
        onChange={(event) => setInstruction(event.target.value)}
        rows={7}
        aria-label="Agent instruction"
      />
      <div className="composer-actions">
        <Button variant="primary" onClick={submit} disabled={busy}>
          {busy ? 'Creating plan' : 'Create agent plan'}
        </Button>
        <span className="muted">Dry run only. No email or call is sent.</span>
      </div>
    </section>
  );
}
