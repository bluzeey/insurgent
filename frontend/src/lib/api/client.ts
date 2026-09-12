import type { InformationRequest, RequestListResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init,
  });
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      detail = body.detail ?? detail;
    } catch {
      // keep HTTP detail
    }
    throw new Error(detail);
  }
  return response.json() as Promise<T>;
}

export const api = {
  listRequests: () => request<RequestListResponse>('/v1/requests'),
  createRequest: (instruction: string) =>
    request<InformationRequest>('/v1/requests', {
      method: 'POST',
      body: JSON.stringify({ instruction, ownerEmail: 'operator@example.com' }),
    }),
  approvePlan: (item: InformationRequest) => {
    if (!item.activePlan) throw new Error('No active plan to approve');
    return request<InformationRequest>(`/v1/requests/${item.id}/approvals`, {
      method: 'POST',
      body: JSON.stringify({ planVersion: item.activePlan.version, planHash: item.activePlan.planHash }),
    });
  },
  control: (id: string, action: 'pause' | 'resume' | 'cancel') =>
    request<InformationRequest>(`/v1/requests/${id}/control`, {
      method: 'POST',
      body: JSON.stringify({ action }),
    }),
  review: (id: string, resultVersion: number, action: 'accept' | 'close_partial', reason?: string) =>
    request<InformationRequest>(`/v1/requests/${id}/reviews`, {
      method: 'POST',
      body: JSON.stringify({ action, resultVersion, reason }),
    }),
};
