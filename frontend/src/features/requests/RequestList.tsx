import { StatusPill } from '../../components/StatusPill';
import type { InformationRequest, RequestListResponse } from '../../lib/api/types';

const groups: Array<{ key: keyof RequestListResponse; label: string }> = [
  { key: 'needsYou', label: 'Needs you' },
  { key: 'running', label: 'Running' },
  { key: 'done', label: 'Done' },
];

export function RequestList({ data, selectedId, onSelect }: { data: RequestListResponse; selectedId?: string; onSelect: (item: InformationRequest) => void }) {
  return (
    <aside className="request-list" aria-label="Agent runs grouped by state">
      {groups.map((group) => (
        <section key={group.key}>
          <h2>{group.label}</h2>
          {data[group.key].length === 0 ? <p className="empty-small">No agent runs.</p> : null}
          {data[group.key].map((item) => (
            <button
              type="button"
              className={`request-row ${item.id === selectedId ? 'selected' : ''}`}
              key={item.id}
              onClick={() => onSelect(item)}
            >
              <span className="request-row-title">{item.activePlan?.objective ?? item.instruction}</span>
              <span className="request-row-meta">
                <StatusPill status={item.status} />
                <span>{item.activePlan?.requestType.replaceAll('_', ' ') ?? 'Unplanned'}</span>
              </span>
            </button>
          ))}
        </section>
      ))}
    </aside>
  );
}
