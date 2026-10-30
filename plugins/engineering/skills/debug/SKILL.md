---
name: debug
description: Structured debugging session — reproduce, isolate, diagnose, and fix. Trigger with an error message or stack trace, "this works in staging but not prod", "something broke after the deploy", or when behavior diverges from expected and the cause isn't obvious.
argument-hint: "<error message or problem description>"
---

# /debug

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run a structured debugging session to find and fix issues systematically.

## Usage

```
/debug $ARGUMENTS
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       DEBUG                                        │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: REPRODUCE                                                │
│  ✓ Understand the expected vs. actual behavior                   │
│  ✓ Identify exact reproduction steps                             │
│  ✓ Determine scope (when did it start? who is affected?)        │
│                                                                    │
│  Step 2: ISOLATE                                                   │
│  ✓ Narrow down the component, service, or code path             │
│  ✓ Check recent changes (deploys, config changes, dependencies) │
│  ✓ Review logs and error messages                                │
│                                                                    │
│  Step 3: DIAGNOSE                                                  │
│  ✓ Form hypotheses and test them                                 │
│  ✓ Trace the code path                                           │
│  ✓ Identify root cause (not just symptoms)                      │
│                                                                    │
│  Step 4: FIX                                                       │
│  ✓ Propose a fix with explanation                                │
│  ✓ Consider side effects and edge cases                          │
│  ✓ Suggest tests to prevent regression                           │
└─────────────────────────────────────────────────────────────────┘
```

## What I Need From You

Tell me about the problem. Any of these help:
- Error message or stack trace
- Steps to reproduce
- What changed recently
- Logs or screenshots
- Expected vs. actual behavior

## Output

```markdown
## Debug Report: [Issue Summary]

### Reproduction
- **Expected**: [What should happen]
- **Actual**: [What happens instead]
- **Steps**: [How to reproduce]

### Root Cause
[Explanation of why the bug occurs]

### Fix
[Code changes or configuration fixes needed]

### Prevention
- [Test to add]
- [Guard to put in place]
```

## If Connectors Available

If **~~monitoring** is connected:
- Pull logs, error rates, and metrics around the time of the issue
- Show recent deploys and config changes that may correlate

If **~~source control** is connected:
- Identify recent commits and PRs that touched affected code paths
- Check if the issue correlates with a specific change

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

- Search for related reports first: `workitem search` in the right workspace, and TRM for user-facing bugs in terminal / liqu-web
- Once the cause is found, draft the fix ticket in the project the code belongs to (MR, OPP, FW, OPS, DX) and, if it came from a TRM bug or an INC incident, a `relates to` relation to it (`workitem_relation list_definitions` to find it)

## Tips

1. **Share error messages exactly** — Don't paraphrase. The exact text matters.
2. **Mention what changed** — Recent deploys, dependency updates, and config changes are top suspects.
3. **Include context** — "This works in staging but not prod" or "Only affects large payloads" narrows things fast.
