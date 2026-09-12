# Implementation phases

## Product direction

The product is now framed as: **create agents for getting insurance workflow data**.

The first agents are:

1. **Form collection agent**: collect basic form data for a workflow.
2. **Clarification agent**: follow up on missing or unclear data.
3. **Renewal changes agent**: check what changed since last year.

Each agent creates a plan. The user approves the plan. The backend runs the collection flow.

## Current implementation: M1 dry run

Built now:

- `frontend/` React, TypeScript, Vite, pnpm.
- `backend/` FastAPI API with fake planning and synthetic results.
- Landing page that explains the agent model.
- Dashboard tabs: My agents, Form collection, Clarification, Renewal changes.
- Agent cards for the first three flows.
- Agent plan preview with respondent, questions, method, limits, and hash.
- Approval endpoint that requires exact plan version and hash.
- Unknown contact blocking before approval.
- Agent run grouping: Needs you, Running, Done.
- Collected data view with answers, gaps, activity, and sources.

Not built yet:

- Real login and tenant isolation.
- PostgreSQL persistence.
- Worker, durable action ledger, and scheduler.
- Real email sending and receiving.
- Document upload.
- Model provider adapter.
- Voice.

## M2 next build slice: durable email loop

1. Replace in memory storage with PostgreSQL.
2. Add tenant, user, and membership authorization.
3. Store immutable agent plans and approvals.
4. Add an outbound action ledger.
5. Add a fake email adapter test suite.
6. Add one live email provider behind a disabled by default flag.
7. Add signed inbound webhooks.
8. Match replies to agent runs.
9. Extract answers with source references.
10. Deliver the final report by email or secure link.

## Gate to move beyond M2

Do not pilot live use until these cases pass:

- Duplicate replies.
- Late replies.
- Conflicting answers.
- Opt out messages.
- Provider outage.
- Wrong recipient risk.
- Stale approval.
- Prompt injection in replies or files.