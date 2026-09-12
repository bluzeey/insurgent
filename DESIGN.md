# Product design system

This application adapts the supplied Anytype reference selectively for an operational insurance-information workspace.

## Decisions

- Use a white canvas, black ink, restrained gray text, hairline borders, flat surfaces, and pill buttons.
- Primary actions use black fill with white text, following the component-token treatment in `anytype.design.md`.
- Use normal-weight operational text for critical request details; do not use ultra-light body copy for statuses, recipients, evidence, or approvals.
- Reserve the serif/editorial moment for the welcome headline only.
- Do not copy Anytype privacy/local-first claims. This product is a backend-driven cloud workflow surface.

## Tokens

- `--ink`: `#000000`
- `--canvas`: `#ffffff`
- `--muted`: `#5b5b5b`
- `--subtle`: `#808080`
- `--line`: `#000000`
- `--line-soft`: `#dedede`
- `--surface-soft`: `#f7f7f4`
- `--mint`: `#3cd9b3`
- `--gradient`: `linear-gradient(165deg,#fff 58%,#ffedbe 78%,#cdffea 90%,#e7d4ff)`

## Components

- Buttons: full pill; black filled primary, outlined secondary.
- Cards: flat, white, 1px hairline, square corners.
- Inputs: 16px radius, black hairline, large touch target.
- Status pills: compact uppercase labels; color is supportive only, not sole meaning.
- Request layout: one workspace composer, grouped worklist, detail pane, contextual actions.

## Prohibited UI expansion for MVP

No KPI dashboard, model selector, visual workflow builder, autonomous-agent avatars, arbitrary tool marketplace, or hidden-recipient outbound action.