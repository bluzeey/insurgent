import type { RequestStatus } from '../lib/api/types';

const labels: Record<RequestStatus, string> = {
  draft: 'Draft',
  preparing: 'Preparing',
  awaiting_approval: 'Awaiting approval',
  queued: 'Queued',
  collecting: 'Collecting',
  waiting: 'Waiting',
  needs_review: 'Needs review',
  ready_for_review: 'Ready for review',
  paused: 'Paused',
  completed: 'Completed',
  closed_partial: 'Closed partial',
  cancelled: 'Cancelled',
  expired: 'Expired',
  failed: 'Failed',
};

export function StatusPill({ status }: { status: RequestStatus }) {
  return <span className={`status status-${status}`}>{labels[status]}</span>;
}
