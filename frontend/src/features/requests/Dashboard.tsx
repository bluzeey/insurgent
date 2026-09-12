import { useEffect, useMemo, useState } from 'react';
import { AgentCatalog } from './AgentCatalog';
import { Composer } from './Composer';
import { RequestDetail } from './RequestDetail';
import { RequestList } from './RequestList';
import { flowCards, type FlowKey } from './flowCopy';
import { api } from '../../lib/api/client';
import type { InformationRequest, RequestListResponse } from '../../lib/api/types';

const emptyData: RequestListResponse = { needsYou: [], running: [], done: [] };
type DashboardTab = 'my_agents' | FlowKey;

export function Dashboard() {
  const [data, setData] = useState<RequestListResponse>(emptyData);
  const [selectedId, setSelectedId] = useState<string>();
  const [activeTab, setActiveTab] = useState<DashboardTab>('my_agents');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  const selected = useMemo(() => {
    const all = [...data.needsYou, ...data.running, ...data.done];
    return all.find((item) => item.id === selectedId) ?? all[0];
  }, [data, selectedId]);

  async function refresh(preferredId?: string) {
    const next = await api.listRequests();
    setData(next);
    if (preferredId) setSelectedId(preferredId);
  }

  async function run(operation: () => Promise<InformationRequest | void>) {
    setBusy(true);
    setError(undefined);
    try {
      const item = await operation();
      await refresh(item?.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setBusy(false);
    }
  }

  function selectFlow(flow: FlowKey) {
    setActiveTab(flow);
  }

  useEffect(() => {
    refresh().catch((err) => setError(err instanceof Error ? err.message : 'Could not load agents'));
  }, []);

  return (
    <main>
      <header className="topbar">
        <a className="wordmark" href="/">Insurgent</a>
        <span className="phase-pill">Dry run</span>
      </header>

      <nav className="dashboard-tabs" aria-label="Dashboard tabs">
        <button className={activeTab === 'my_agents' ? 'active' : ''} type="button" onClick={() => setActiveTab('my_agents')}>
          My agents
        </button>
        {flowCards.map((flow) => (
          <button key={flow.flow} className={activeTab === flow.flow ? 'active' : ''} type="button" onClick={() => selectFlow(flow.flow)}>
            {flow.title.replace(' agent', '')}
          </button>
        ))}
      </nav>

      {activeTab === 'my_agents' ? (
        <div className="dashboard-simple">
          <AgentCatalog onSelectFlow={selectFlow} />
          <aside className="recent-panel">
            <h2>Recent agent runs</h2>
            <RequestList data={data} selectedId={selected?.id} onSelect={(item) => setSelectedId(item.id)} />
          </aside>
        </div>
      ) : (
        <div className="workspace">
          <div className="left-rail">
            <Composer flow={activeTab} onSubmit={(instruction) => run(() => api.createRequest(instruction))} busy={busy} />
            {error ? <div className="error" role="alert">{error}</div> : null}
            <RequestList data={data} selectedId={selected?.id} onSelect={(item) => setSelectedId(item.id)} />
          </div>
          <RequestDetail
            item={selected}
            busy={busy}
            onApprove={(item) => run(() => api.approvePlan(item))}
            onCancel={(item) => run(() => api.control(item.id, 'cancel'))}
            onClosePartial={(item) => run(() => api.review(item.id, item.result?.version ?? 1, 'close_partial', 'Closed after dry run.'))}
          />
        </div>
      )}
    </main>
  );
}
