export type FlowKey = 'form_collection' | 'clarification' | 'renewal_changes';

export const flowCards: Array<{
  flow: FlowKey;
  label: string;
  title: string;
  description: string;
  example: string;
}> = [
  {
    flow: 'form_collection',
    label: 'Flow 1',
    title: 'Form collection agent',
    description: 'Collect the basic form data needed to start an insurance workflow.',
    example: "Create a form collection agent. Ask the client's finance contact for current turnover, business activity, and locations. Email only.",
  },
  {
    flow: 'clarification',
    label: 'Flow 2',
    title: 'Clarification agent',
    description: 'Ask follow up questions when figures, dates, or documents are missing.',
    example: "Create a clarification agent. Ask the client's finance contact for the missing figures, reporting period, and source document. Email only.",
  },
  {
    flow: 'renewal_changes',
    label: 'Flow 3',
    title: 'Renewal changes agent',
    description: 'Check what changed since last year before a renewal is processed.',
    example: "Create a renewal changes agent. Ask the client's finance contact whether turnover, activity, or locations changed since last year. Email only.",
  },
];

export function getFlowCard(flow: FlowKey) {
  return flowCards.find((item) => item.flow === flow) ?? flowCards[0];
}
