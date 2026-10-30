# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~source control` might mean GitHub, GitLab, or any other VCS with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (source control, CI/CD, monitoring, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams |
| Source control | `~~source control` | GitHub | GitLab, Bitbucket |
| Project tracker | — | **Plane** (LIQ and YEVA workspaces) | — |
| Knowledge base | `~~knowledge base` | Notion | Confluence, Guru, Coda |
| Monitoring | `~~monitoring` | Datadog | New Relic, Grafana, Splunk |
| Incident management | — | **Plane** (INC project in each workspace) | — |
| CI/CD | `~~CI/CD` | — | CircleCI, GitHub Actions, Jenkins, BuildKite |

## Plane

This plugin is set up for Plane as both the project tracker and the incident tracker.

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

Exchange (LIQ) MR states: Backlog → Todo → In Progress → In Review (PR open, PR link as a comment) → On staging (merged to staging, not yet in main) → Done · Cancelled. Weekly cycles are named "Неделя N" and their description holds the week's goals.
ops-platform (YEVA) OPP states: Backlog → Todo → In Progress → In Review → Done · Cancelled. No cycles yet.
Incidents (INC, both workspaces): New → In Progress → Mitigated → Done · Cancelled.
