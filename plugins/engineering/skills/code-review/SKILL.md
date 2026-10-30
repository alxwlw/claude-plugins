---
name: code-review
description: Review code changes for security, performance, and correctness. Trigger with a PR URL or diff, "review this before I merge", "is this code safe?", or when checking a change for N+1 queries, injection risks, missing edge cases, or error handling gaps.
argument-hint: "<PR URL, diff, or file path>"
---

# /code-review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Review code changes with a structured lens on security, performance, correctness, and maintainability.

## Usage

```
/code-review <PR URL or file path>
```

Review the provided code changes: @$1

If no specific file or URL is provided, ask what to review.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      CODE REVIEW                                   │
├─────────────────────────────────────────────────────────────────┤
│  STANDALONE (always works)                                       │
│  ✓ Paste a diff, PR URL, or point to files                      │
│  ✓ Security audit (OWASP top 10, injection, auth)               │
│  ✓ Performance review (N+1, memory leaks, complexity)           │
│  ✓ Correctness (edge cases, error handling, race conditions)    │
│  ✓ Style (naming, structure, readability)                        │
│  ✓ Actionable suggestions with code examples                    │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect your tools)                      │
│  + Source control: Pull PR diff automatically                    │
│  + Plane: Link findings to work items                            │
│  + Knowledge base: Check against team coding standards           │
└─────────────────────────────────────────────────────────────────┘
```

## Review Dimensions

### Security
- SQL injection, XSS, CSRF
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure deserialization
- Path traversal
- SSRF

### Performance
- N+1 queries
- Unnecessary memory allocations
- Algorithmic complexity (O(n²) in hot paths)
- Missing database indexes
- Unbounded queries or loops
- Resource leaks

### Correctness
- Edge cases (empty input, null, overflow)
- Race conditions and concurrency issues
- Error handling and propagation
- Off-by-one errors
- Type safety

### Maintainability
- Naming clarity
- Single responsibility
- Duplication
- Test coverage
- Documentation for non-obvious logic

## Output

```markdown
## Code Review: [PR title or file]

### Summary
[1-2 sentence overview of the changes and overall quality]

### Critical Issues
| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| 1 | [file] | [line] | [description] | 🔴 Critical |

### Suggestions
| # | File | Line | Suggestion | Category |
|---|------|------|------------|----------|
| 1 | [file] | [line] | [description] | Performance |

### What Looks Good
- [Positive observations]

### Verdict
[Approve / Request Changes / Needs Discussion]
```

## If Connectors Available

If **~~source control** is connected:
- Pull the PR diff automatically from the URL
- Check CI status and test results

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

- Find the work item the PR implements (an identifier like `MR-244` in the branch, title or description) and check the PR against its description and acceptance criteria
- Point out scope that the work item does not cover, and anything it asks for that the PR misses
- Offer to add the review summary as a comment on the work item, and to move it to In Review with the PR link as a comment if it is not there yet

If **~~knowledge base** is connected:
- Check changes against team coding standards and style guides

## Tips

1. **Provide context** — "This is a hot path" or "This handles PII" helps me focus.
2. **Specify concerns** — "Focus on security" narrows the review.
3. **Include tests** — I'll check test coverage and quality too.
