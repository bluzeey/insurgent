export type RequestStatus =
  | 'draft'
  | 'preparing'
  | 'awaiting_approval'
  | 'queued'
  | 'collecting'
  | 'waiting'
  | 'needs_review'
  | 'ready_for_review'
  | 'paused'
  | 'completed'
  | 'closed_partial'
  | 'cancelled'
  | 'expired'
  | 'failed';

export type UiGroup = 'needs_you' | 'running' | 'done';
export type RequestType = 'initial_collection' | 'clarification' | 'renewal_changes';

export interface Contact {
  id: string;
  name: string;
  organization: string;
  email: string;
  role: string;
  authorized: boolean;
  suppressed: boolean;
}

export interface Question {
  id: string;
  label: string;
  required: boolean;
  dataType: string;
  unitsHint?: string | null;
  periodHint?: string | null;
  evidenceRule: string;
}

export interface RequestPlan {
  version: number;
  objective: string;
  requestType: RequestType;
  respondent: null | {
    contactId: string;
    name: string;
    organization: string;
    email: string;
  };
  questions: Question[];
  alreadyAvailable: string[];
  method: {
    channel: 'email';
    reminderCount: number;
    reminderAfterHours: number;
  };
  limits: {
    deadline: string;
    maxTouches: number;
    forbiddenChannels: string[];
  };
  deliverable: string;
  blockingClarifications: string[];
  planHash: string;
}

export interface Event {
  sequence: number;
  type: string;
  message: string;
  createdAt: string;
}

export interface Answer {
  questionId: string;
  question: string;
  rawValue: string | null;
  normalizedValue?: string | null;
  status: 'open' | 'answered' | 'unavailable' | 'conflicting' | 'waived';
  evidenceStatus?: 'reported' | 'document_supported' | 'human_confirmed' | null;
  source?: string | null;
}

export interface RequestResult {
  version: number;
  status: 'complete' | 'partial';
  summary: string;
  answers: Answer[];
  unresolvedItems: string[];
  generatedAt: string;
}

export interface InformationRequest {
  id: string;
  instruction: string;
  status: RequestStatus;
  uiGroup: UiGroup;
  ownerEmail: string;
  createdAt: string;
  updatedAt: string;
  version: number;
  activePlan: RequestPlan | null;
  result: RequestResult | null;
  allowedActions: string[];
  events: Event[];
}

export interface RequestListResponse {
  needsYou: InformationRequest[];
  running: InformationRequest[];
  done: InformationRequest[];
}
