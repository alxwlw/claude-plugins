---
name: architecture
description: Create or evaluate an architecture decision record (ADR). Use when choosing between technologies (e.g., Kafka vs SQS), documenting a design decision with trade-offs and consequences, reviewing a system design proposal, or designing a new component from requirements and constraints.
argument-hint: "<decision or system to design>"
---

# /architecture

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Create an Architecture Decision Record (ADR) or evaluate a system design.

## Usage

```
/architecture $ARGUMENTS
```

## Modes

**Create an ADR**: "Should we use Kafka or SQS for our event bus?"
**Evaluate a design**: "Review this microservices proposal"
**System design**: "Design the notification system for our app"

See the **system-design** skill for detailed frameworks on requirements gathering, scalability analysis, and trade-off evaluation.

## Output — ADR Format

```markdown
# ADR-[number]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [Date]
**Deciders:** [Who needs to sign off]

## Context
[What is the situation? What forces are at play?]

## Decision
[What is the change we're proposing?]

## Options Considered

### Option A: [Name]
| Dimension | Assessment |
|-----------|------------|
| Complexity | [Low/Med/High] |
| Cost | [Assessment] |
| Scalability | [Assessment] |
| Team familiarity | [Assessment] |

**Pros:** [List]
**Cons:** [List]

### Option B: [Name]
[Same format]

## Trade-off Analysis
[Key trade-offs between options with clear reasoning]

## Consequences
- [What becomes easier]
- [What becomes harder]
- [What we'll need to revisit]

## Action Items
1. [ ] [Implementation step]
2. [ ] [Follow-up]
```

## If Connectors Available

If **~~knowledge base** is connected:
- Search for prior ADRs and design docs
- Find relevant technical context

If **Plane** is connected:
**Plane routing.** There are two Plane workspaces, each with its own connector. Pick by repository, then by project:

| Repository | Workspace (tools) | Project |
|---|---|---|
| liqu-fi exchange code: monorepo, synthetix-v3, synthetix-deployments, terminal, liqu-web | LIQ (`Plane_LIQ`) | MR — engineering backlog |
| Product bugs in terminal / liqu-web | LIQ | TRM — bugs, Intake only; root cause goes to MR or OPS |
| Live-system work for the exchange | LIQ | OPS |
| Dev tooling shared by both teams (plane-hooks, dev-agent, stack, CI runner) | LIQ | DX — also for yeva tooling |
| Claude Code / plan-loop harness | LIQ | HRN |
| liqu-fi/legwork | LIQ | LW |
| yevaops/ops-platform | YEVA (`Plane_YEVA`) | OPP |
| yevaops/framework | YEVA | FW |
| Live-system work for ops-platform | YEVA | OPS |
| yulii/gcs | YEVA | GCS — stages and customer only; engineering tickets live in the repo (docs/wayfinder/) |

Never read or write the YEVA project SLU (military): it is not engineering work. If the repository is unclear, ask which workspace.
Work item references look like `MR-244` or `OPP-12`: open them with `workitem retrieve_by_identifier` on the matching workspace. List a project's states with `state list` before moving anything — do not assume names.
**Writes need confirmation:** show the draft (project, title, description, state, relations) and create or change it in Plane only after the user says yes. Write titles and comments in Russian, like the existing items.

- Link the ADR to related work: the module (arc / direction) and any Epic work items in the project
- Draft implementation tasks in the matching project and module, ordered, with `blocked_by` relations where one task depends on another; create them only after confirmation

## Tips

1. **State constraints upfront** — "We need to ship in 2 weeks" or "Must handle 10K rps" shapes the answer.
2. **Name your options** — Even if you're leaning one way, I'll give a more balanced analysis with explicit alternatives.
3. **Include non-functional requirements** — Latency, cost, team expertise, and maintenance burden matter as much as features.
