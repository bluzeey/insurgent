# Implementation phases

## Current implementation: M1 contract-first dry run

Built now:

- Top-level `frontend/` React + TypeScript + Vite workspace.
- Top-level `backend/` FastAPI API with deterministic fake planning and synthetic results.
- Three shared template configs: initial collection, clarification, renewal changes.
- Bounded plan preview with exact respondent, questions, channel, limits, and hash.
- Approval endpoint that requires exact plan version/hash.
- Ambiguous recipient blocking before approval.
- Request grouping: Needs you, Running, Done.
- Result review surface showing answers, gaps, activity, and evidence notes.

Not built yet:

- Real authentication/tenant isolation.
- PostgreSQL/Alembic persistence.
- Celery/Redis worker, durable action ledger, scheduler.
- Real email sending/receiving or document upload.
- Model provider adapter.
- Voice.

## M2 next build slice: durable email loop

1. Replace in-memory store with PostgreSQL repositories.
2. Add tenant/user/membership models and server-derived authorization.
3. Add immutable plan versions and approval records.
4. Add outbound action ledger and due-action dispatcher.
5. Add fake-email adapter tests, then one live email provider behind a disabled-by-default flag.
6. Add signed webhook ingestion, deduplication, reply correlation, and opt-out suppression.
7. Add answer extraction adapter with fixed regression fixtures.
8. Add report delivery as a separate state from collection completion.

## Gate to move beyond M2

Do not pilot live use until duplicate, late, conflicting, opt-out, outage, wrong-recipient, stale-approval, and prompt-injection tests pass.