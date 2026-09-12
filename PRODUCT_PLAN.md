# Product plan
## A small interface for completing information requests across insurance workflows

**Owner:** Sahil Maheshwari · **Version:** 0.1 · **Status:** Proposed pilot plan

## 1. The product decision

Build an **English-first information-collection assistant for insurance professionals**. A person describes a purpose and an information gap. The system converts that instruction into a bounded request, uses existing context, contacts an approved respondent, asks relevant follow-ups, and returns a structured, source-linked summary by email.

This is not an underwriting dashboard, an autonomous claims engine, a generic chatbot, or a visual agent builder. The customer does not configure prompts, models, tools, chains, or workflow nodes. Their work is to express intent and approve meaningful actions.

The repeatable unit is:

**Purpose + approved respondent + existing context + required information + limits → collection → clarification → result.**

A request may start a process or unblock an existing one. Several request types share the same execution engine. This preserves your multi-flow thesis without requiring a different application for property submissions, renewals, or document follow-ups. [P1]

## 2. What the user actually does

A broker writes:

> Ask the client's finance contact for the three missing figures in this email. We already have last year's turnover. Ask for this year's figure and the reporting period, remind them once if necessary, and email me the answers. Don't call.

The system extracts the intended task and shows a short plan:

**Who:** the resolved contact's name, organization, and exact email.  
**Collect:** the three named figures, including their period and units.  
**Already available:** last year's turnover, shown with its original source and date.  
**Method:** email; one reminder after the displayed interval; no calls.  
**Deliver:** a summary to the requester, with unanswered items and sources.  
**Limits:** deadline, approved data scope, and contact/cost cap.

The user selects **Approve and start**. Work continues server-side even when the tab closes. The operator returns only for an exception, a requested change, or result review. A summary still arrives in their inbox; the dashboard is a control surface, not a compulsory replacement for email.

The system must never turn an unclear name into a guessed recipient or turn “handle the renewal” into authority to recommend terms. Ambiguity about identity, authority, or material data scope causes a targeted question before external action.

## 3. Why this fits the project

Your stated advantage is product engineering, not independent insurance judgment. You want leverage across workflows and are concerned that customer-specific implementation will turn a one-person business into an expensive deployment service. The plan therefore standardizes **request execution**, not the substance of every insurance decision. [P1]

The recovered research describes broker information gathering, clarification, changing risk facts, and claims-related process/evidence problems. It also explicitly records missing evidence on a paying buyer, production access, and repeatable economics. These observations justify testing this product, not declaring it validated. [P4]

Atmaram's property-flow recap supports collecting and updating risk information around a broker's work. Erick's recap supports the existence of questionnaires and confirmation work, but his US/Latin American examples should not be treated as Indian frequency or cost benchmarks. Rohan distinguishes placement data from claims evidence. Jyoti's observations warn that some failures are about procedure and specialist judgment, not merely an unanswered form. [P4]

**Design implication:** source-backed questions and controlled follow-up are in scope. Replacing the broker, determining coverage, deciding a claim, or asserting that a complete form equals a complete risk assessment are not.

## 4. The first customer hypothesis

Start with **one commercial-broking account or operations team that handles several information requests for existing clients**. The proposed operator is the account executive or servicing coordinator. A team lead reviews templates and permissions; a branch, operations, or business owner is the budget hypothesis. None is yet a confirmed buyer.

A broker is a useful initial hypothesis because the same team may own initial gathering, insurer follow-ups, and renewal updates. Test that ownership in real cases. Do not assume an underwriter has permission to bypass the broker and contact the insured directly.

Select design partners through your existing insurance conversations and workshops, rather than requiring a new broad acquisition campaign. Workshop attendance is evidence of interest in learning, not purchase intent. Seek someone willing to show actual redacted threads, identify a process owner, and run a bounded trial.

## 5. What “multi-flow” means in the first release

Prove these three jobs with the same UI, data model, and execution code:

| Request type | Timing | Job | Output |
|---|---|---|---|
| Initial collection | Beginning | Collect an expert-provided information checklist | Answers, evidence references, and remaining gaps |
| Clarification | Middle | Resolve explicitly missing or inconsistent details in an existing request | A response pack mapped to each open question |
| Renewal changes | Later lifecycle | Ask whether approved prior facts changed, without assuming they remain current | A dated change/no-change/unknown summary |

Claims-document follow-up and administrative D&O information collection are **controlled extension tests**, not implied first-release expertise. They can reuse the engine, but require different approved questions, evidence rules, confidentiality controls, and reviewers.

Multi-flow does not mean arbitrary enterprise automation. Keep one main respondent per request in the first pilot. A second respondent becomes a separate linked request, not an autonomous delegation tree. This is a scope limit on coordination complexity, not a limit to one business workflow.

## 6. The smallest useful interface

**Workspace:** a large instruction box, optional attachments, and a list of requests grouped as Needs you, Running, and Done. Three example instructions help users begin. There are no KPI tiles, model settings, agent avatars, or flow charts.

**Request detail:** objective, current status, next planned action, collected answers, remaining gaps, and a collapsed activity/evidence section. One contextual primary action appears when needed. Pause is always reachable.

**Settings:** identity/sender setup, a small authorized contact directory, permitted channels, and notification defaults. Advanced risk limits are set by the team owner and displayed in the approval card, not exposed as a complicated control panel for every request.

Natural language is the main control mechanism, but buttons remain for reliable, obvious actions such as approve, pause, and close. “Minimal UI” must not mean hiding recipients, erasing uncertainty, or making users type a command to stop a running process.

## 7. Use the Anytype reference selectively

Use the supplied file's neutral canvas, restrained sans-serif typography, hairlines, flat surfaces, pill buttons, and optional pastel empty-state treatment. Preserve the original reference unchanged. [P3]

The file is a marketing design reference, not a complete application specification. It also conflicts internally: several prose passages describe an outlined primary button, while the component tokens prescribe black fill with white text. This plan deliberately chooses the component-token treatment for the main action and documents that decision in `DESIGN.md`.

Use normal operational body weight rather than ultra-light text for critical details. Reserve any editorial-serif moment for the welcome state. Do not copy Anytype's local-first or “data stays on your device” claims into a backend-driven cloud product. No proprietary font files are included.

## 8. Backend-first implementation

Use **React + TypeScript + Vite** for a thin client. Use **Python + FastAPI**, a relational database, a worker, and explicit integration adapters behind it. React's official guidance includes a build-from-scratch path using tools such as Vite; choosing it here is a product architecture decision because the application already has a dedicated Python backend. [T1]

The proposed backend is a modular monolith, deployed as an API and worker from one codebase. PostgreSQL owns durable request state, plan versions, evidence, approvals, schedules, and an outbound-action ledger. Celery with Redis handles dispatch and retries; it is not the only record of scheduled work. Document bytes live in object storage.

A model interprets instructions, proposes questions, extracts answers, and drafts summaries. **Code** controls recipients, permissions, permitted channels, rate limits, budgets, state transitions, and whether an action may execute. A plan must pass schema and domain checks; structurally valid output is not evidence that an insurance fact is true. [T2]

Email comes first as a complete loop: send, receive, reconcile, ask follow-up, stop, and report. Voice is a later live adapter on the same contract, not a separate product. Its initial proof can use synthetic conversations or uploaded authorized call notes. Do not claim live calling until provider capability, recipient permissions, call handling, and relevant launch checks pass.

## 9. Delivery sequence and exit gates

| Gate | Deliverable | Do not advance until… |
|---|---|---|
| G0 — Observe | Redacted examples from several request types | A process owner confirms the work, channel, and useful output |
| G1 — Dry run | Instruction → valid plan → mock reply → structured result | Three templates run through one engine; ambiguous recipients cannot launch |
| G2 — Email loop | Approved send and reply ingestion with durable state | Duplicate, late, conflicting, opt-out, and outage tests pass |
| G3 — Multi-flow pilot | The same team uses three request types | Reuse, review burden, respondent experience, and economics are measured |
| G4 — Voice option | Approved short call returns evidence into the same request | Voice adds measurable value and all provider/safety gates pass |
| G5 — Productize | Repeatable onboarding and a paid continuation decision | Repeated use does not require customer-specific execution code |

These are proposed delivery phases, not promised completion dates. Document observations after every gate. The backlog gives build-sized stories and acceptance criteria.

## 10. What would count as success

The primary outcome is **useful information returned with less total human handling**, not the number of calls made or fields populated. Measure operator preparation, review, correction, and escalation time; include respondent burden rather than merely moving work to the client.

Proposed pilot targets include: at least 30% lower median operator handling time in comparable cases, no critical unsupported facts in accepted reports, no unauthorized outbound actions, and successful use of three templates without new orchestration code. These are decision thresholds to test, not current performance claims. A small sample is directional, not statistical proof.

Track value per team across workflows. Several low-volume uses may together justify one subscription, but do not assume adding workflow counts increases willingness to pay. Test a paid continuation against measured benefit, and include setup/support time in the economics.

## 11. Main criticism of the thesis

The biggest risk is that information is missing because the respondent does not know it, cannot disclose it, needs approval, or lacks the document. A more fluent reminder does not remove that constraint. A useful result may be “the finance team must approve release,” not a filled field.

The second risk is that each workflow requires so much bespoke insurance logic that the shared engine is a thin wrapper. Track template setup and exception work explicitly. Stop adding workflow breadth if it disguises an implementation business.

The third is adoption: an unfamiliar AI sender or call may get fewer useful responses than a known broker. Preserve the broker's identity and authority, make the automation transparent, and measure completion against the existing method.

**Recommended commitment:** build one reusable information-request product, demonstrate three bounded workflows, and expand only when the shared capability—not custom services—creates the value.
