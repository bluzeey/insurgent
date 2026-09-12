# Insurgent

Create agents for getting insurance workflow data.

The app is intentionally simple. A user chooses an agent, reviews the plan, approves the run, and gets collected data back with gaps and sources.

## Simple product model

- **My agents**: the place to create and reuse data collection agents.
- **Form collection agent**: collects basic form data needed to start a workflow.
- **Clarification agent**: follows up on missing figures, dates, units, or documents.
- **Renewal changes agent**: checks what changed since last year.

An agent is a safe preset for collecting data. It is not an autonomous insurance decision maker.

## What is built now

- `frontend/`: React, TypeScript, Vite, pnpm.
- `backend/`: FastAPI dry run API.
- `contracts/`: plan and result schemas.
- `DESIGN.md`: product design notes.
- `IMPLEMENTATION_PHASES.md`: build phases.

No real emails, calls, or provider actions are sent in this version.

## Routes

- `/`: landing page.
- `/dashboard`: agent dashboard.

## Run locally

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
corepack enable
pnpm install
pnpm dev
```

The frontend expects the API at `http://localhost:8000`. Override with `VITE_API_BASE_URL` if needed.

## Try it

1. Open `/dashboard`.
2. Go to `My agents`.
3. Choose `Form collection agent`.
4. Review the generated plan.
5. Approve the agent plan.
6. Review the sample collected data.

## Safety boundaries

- No agent contacts anyone before approval.
- Unknown contacts block the run.
- Approval requires the exact plan version and hash.
- The current result is synthetic sample data.
- All three agent types use the same backend flow.

## Next phase

The next build phase is the durable email loop: database persistence, approved email sending, signed inbound webhooks, reply matching, source backed extraction, and report delivery.