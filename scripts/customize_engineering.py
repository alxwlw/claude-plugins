"""Apply the Plane customization to a fresh copy of the upstream engineering plugin.

Usage: python3 customize_engineering.py <path-to-engineering-plugin>

Every replacement asserts that it matched exactly once, so if upstream rewrites a
section this script stops instead of silently skipping it. Fix the pattern below,
then run scripts/update-engineering.sh again.
"""
import pathlib, re, json, sys

root = pathlib.Path(sys.argv[1])


def replace_once(path, old, new):
    t = path.read_text()
    assert t.count(old) == 1, (str(path), old[:60], t.count(old))
    path.write_text(t.replace(old, new))


ROUTING = """\
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
"""

SECTIONS = {
    "debug": (
        r"If \*\*~~project tracker\*\* is connected:\n- Search for related bug reports or known issues\n- Create a ticket for the fix once identified\n",
        "If **Plane** is connected:\n" + ROUTING + """
- Search for related reports first: `workitem search` in the right workspace, and TRM for user-facing bugs in terminal / liqu-web
- Once the cause is found, draft the fix ticket in the project the code belongs to (MR, OPP, FW, OPS, DX) and, if it came from a TRM bug or an INC incident, a `relates to` relation to it (`workitem_relation list_definitions` to find it)
""",
    ),
    "code-review": (
        r"If \*\*~~project tracker\*\* is connected:\n- Link findings to related tickets\n- Verify the PR addresses the stated requirements\n",
        "If **Plane** is connected:\n" + ROUTING + """
- Find the work item the PR implements (an identifier like `MR-244` in the branch, title or description) and check the PR against its description and acceptance criteria
- Point out scope that the work item does not cover, and anything it asks for that the PR misses
- Offer to add the review summary as a comment on the work item, and to move it to In Review with the PR link as a comment if it is not there yet
""",
    ),
    "architecture": (
        r"If \*\*~~project tracker\*\* is connected:\n- Link to related epics and tickets\n- Create implementation tasks\n",
        "If **Plane** is connected:\n" + ROUTING + """
- Link the ADR to related work: the module (arc / direction) and any Epic work items in the project
- Draft implementation tasks in the matching project and module, ordered, with `blocked_by` relations where one task depends on another; create them only after confirmation
""",
    ),
    "standup": (
        r"If \*\*~~project tracker\*\* is connected:\n- Pull tickets moved to \"in progress\" or \"done\"\n- Show upcoming sprint items\n",
        "If **Plane** is connected:\n" + ROUTING + """
- Pull the user's work items in both workspaces that changed state since the last standup (`assignee = currentUser()`), and name them by identifier
- Count an exchange item as shipped only in Done; In Review and On staging (merged to staging, not yet promoted to main) go under in progress
- For the exchange, read the current weekly cycle in MR ("Неделя N"): its description lists the week's goals; show what is left of it under Today. YEVA has no cycles yet — use the user's open items there
""",
    ),
    "incident-response": (
        r"If \*\*~~incident management\*\* is connected:\n- Create or update incident in PagerDuty/Opsgenie\n- Page on-call responders\n",
        "If **Plane** is connected (incidents live in the INC projects):\n" + ROUTING + """
- Exchange incidents: LIQ project INC. plane-hooks opens them automatically from Grafana alerts and failed deploys (labels `alert` and `deploy-failed`), so look for an existing one before drafting a new item
- ops-platform incidents: YEVA project INC, opened by hand
- Move the incident through New → In Progress → Mitigated → Done (or Cancelled) as the response goes, and add status updates as comments
- Postmortem action items become work items in OPS (operational root cause) or MR / OPP (code root cause), each with a `relates to` relation to the incident
- Plane does not page anyone: tell the user who to contact rather than claiming on-call was paged
""",
    ),
    "deploy-checklist": (
        r"(If \*\*~~monitoring\*\* is connected:\n- Pre-fill rollback trigger thresholds from current baselines\n- Set up post-deploy metric watch\n)",
        r"""\1
If **Plane** is connected:
""" + ROUTING.replace("\\", "\\\\") + """
- For an exchange release, list the MR items in On staging: these are what the promotion to main ships. Flag any temporary workaround that must be reverted before it goes to prod
- After the promotion, offer to move those items to Done; a failed deploy will already have an INC item from plane-hooks
""",
    ),
}

for skill, (pattern, repl) in SECTIONS.items():
    p = root / "skills" / skill / "SKILL.md"
    text = p.read_text()
    new, n = re.subn(pattern, repl, text)
    assert n == 1, (skill, n)
    p.write_text(new)

# Deploy checklist template line
replace_once(root / "skills/deploy-checklist/SKILL.md", "- [ ] Close related tickets", "- [ ] Move shipped work items to Done in Plane")

# ASCII box lines in skills mentioning project tracker
replace_once(root / "skills/code-review/SKILL.md",
             "│  + Project tracker: Link findings to tickets                     │",
             "│  + Plane: Link findings to work items                            │")
replace_once(root / "skills/standup/SKILL.md",
             "│  + Project tracker: Ticket status changes                        │",
             "│  + Plane: Work item state changes                                │")

# CONNECTORS.md
p = root / "CONNECTORS.md"
replace_once(p, "| Project tracker | `~~project tracker` | Linear, Asana, Atlassian (Jira/Confluence) | Shortcut, ClickUp |",
             "| Project tracker | — | **Plane** (LIQ and YEVA workspaces) | — |")
replace_once(p, "| Incident management | `~~incident management` | PagerDuty | Opsgenie, Incident.io, FireHydrant |",
             "| Incident management | — | **Plane** (INC project in each workspace) | — |")
t = p.read_text()
t += "\n## Plane\n\nThis plugin is set up for Plane as both the project tracker and the incident tracker.\n\n" + ROUTING + """
Exchange (LIQ) MR states: Backlog → Todo → In Progress → In Review (PR open, PR link as a comment) → On staging (merged to staging, not yet in main) → Done · Cancelled. Weekly cycles are named "Неделя N" and their description holds the week's goals.
ops-platform (YEVA) OPP states: Backlog → Todo → In Progress → In Review → Done · Cancelled. No cycles yet.
Incidents (INC, both workspaces): New → In Progress → Mitigated → Done · Cancelled.
"""
p.write_text(t)

# README connector rows
p = root / "README.md"
replace_once(p, "| **Project tracker** | Linear, Jira, Asana | Ticket status, sprint data, assignments |",
             "| **Project tracker** | Plane (LIQ, YEVA) | Work item states, weekly cycles, assignments, incidents (INC) |")
replace_once(p, "| **Incident management** | PagerDuty, Opsgenie | On-call schedules, incident tracking, paging |",
             "| **Incident management** | Plane (INC in LIQ and YEVA) | Incident tracking, status updates, follow-up work items |")

# Manifest: keep the name, label it, and drop version so every commit to the marketplace reaches users
p = root / ".claude-plugin" / "plugin.json"
m = json.loads(p.read_text())
m.pop("version", None)
m["displayName"] = "Engineering (Plane)"
p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

# .mcp.json: replace the trackers with the two Plane connectors. The URLs must match the
# account's custom connectors exactly, or claude.ai offers to add them as new connectors.
p = root / ".mcp.json"
cfg = json.loads(p.read_text())
for k in ["linear", "asana", "pagerduty"]:
    cfg["mcpServers"].pop(k, None)
servers = {
    "Plane [LIQ]": {"type": "http", "url": "https://plane-mcp.liqu.si/http/mcp"},
    "Plane [YEVA]": {"type": "http", "url": "https://plane-mcp.liqu.si/http/mcp?workspace=yeva-egn"},
}
servers.update(cfg["mcpServers"])
cfg["mcpServers"] = servers
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("ok")
