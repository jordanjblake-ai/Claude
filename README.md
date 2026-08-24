# Life OS

A personal, AI-driven life operating system: one CEO agent, five specialist sub-agents,
and a data layer that fills itself.

The design goal is **zero manual data entry**. Anything you have to type twice will
eventually stop being typed at all, so the system is built around sensors, APIs and
scheduled agents rather than forms and habit-tracking discipline.

## Start here

| Document | What it covers |
| --- | --- |
| [docs/life-os/architecture.md](docs/life-os/architecture.md) | The layered design, the agent roster, and how conflicts between agents are resolved |
| [docs/life-os/discovery-interview.md](docs/life-os/discovery-interview.md) | Phase 1: the structured onboarding interview, in rounds of 3–4 questions |
| [docs/life-os/integration-map.md](docs/life-os/integration-map.md) | Phase 2: every data source, the API that reaches it, and what it costs to wire up |
| [docs/life-os/rollout.md](docs/life-os/rollout.md) | The sequenced build plan, quick wins first |
| [profile/profile.yaml](profile/profile.yaml) | The single source of truth every agent reads before it acts |

## The agent roster

The CEO agent runs in the main conversation; its doctrine lives in [CLAUDE.md](CLAUDE.md).
The five specialists are real Claude Code sub-agents in [.claude/agents/](.claude/agents/):

- **finance-cfo** — cash flow, net worth, subscription leakage, savings targets
- **health-coach** — weight, training load, sleep, recovery, the trend behind the noise
- **relationship-concierge** — contact cadence, dates that matter, gifts, follow-through
- **ai-scout** — tracks AI releases and filters them down to what changes your work
- **quest-master** — hobbies and long-horizon goals, protected against urgent-but-trivial

## Current state

Phase 1 (Discovery) is open. The interview in
[discovery-interview.md](docs/life-os/discovery-interview.md) is unanswered, and
`profile/profile.yaml` is a template full of `TODO` markers. Every agent is written to
degrade gracefully against an unfilled profile: it will tell you which field it needed
rather than inventing an answer.
