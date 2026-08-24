# Architecture

## The design constraint that drives everything

Every personal-productivity system that has ever failed, failed at the same place: the
human stopped typing. Not because they stopped caring, but because manual capture is a
tax paid daily for a benefit received quarterly.

So the ordering rule for this system is: **a data point that cannot be captured
automatically is a data point the system should not depend on.** Where automatic
capture is impossible, the fallback is not a form — it is an agent that asks one
question at a moment when you are already talking to it.

## The five layers

```
┌─ Layer 4 · Surfaces ─────────────────────────────────────────┐
│  Daily brief · Weekly review · Monthly close · Ad-hoc query  │
├─ Layer 3 · CEO Agent ────────────────────────────────────────┤
│  Delegation · Arbitration · Synthesis · Cadence              │
├─ Layer 2 · Specialists ──────────────────────────────────────┤
│  finance-cfo · health-coach · relationship-concierge         │
│  ai-scout · quest-master                                     │
├─ Layer 1 · Ledger ───────────────────────────────────────────┤
│  Notion databases · Google Sheets · profile/profile.yaml     │
├─ Layer 0 · Capture ──────────────────────────────────────────┤
│  Bank aggregator · Smart scale · Wearable · Calendar         │
│  Contacts · RSS/arXiv · GitHub · Email receipts              │
└──────────────────────────────────────────────────────────────┘
```

Layers 0 and 1 are the whole game. Layers 2–4 are prompts, and prompts are cheap to
change. Getting the capture pipes right is the work that actually compounds, which is
why Phase 2 is a data-mapping phase and not a prompt-writing phase.

## What is already live

This matters more than it might look. The owner's Claude environment already has
connectors for **Gmail, Google Calendar, Google Drive, Notion and GitHub**. That means
for a meaningful slice of the system, Claude *is* the integration layer — there is no
Make scenario to build, no Zapier task quota to spend, and no webhook to debug.

Concretely, these work on day one with no new infrastructure:

- Calendar read/write → the health-coach can see whether a training block survived the
  week, and the concierge can schedule the call it is nagging you about.
- Gmail search → receipts, renewal notices and subscription confirmations are already
  sitting in the inbox as a financial data source.
- Notion → the ledger. Databases for people, goals, weight, and the AI watchlist.
- Drive → CSV exports from anything that refuses to offer an API.

The middleware discussion (Make vs. n8n vs. Zapier) only becomes necessary for the
sources Claude cannot reach directly: the bank, the scale, and the wearable. See
[integration-map.md](integration-map.md).

## Agent boundaries

Each specialist owns a domain end to end — its data sources, its ledger tables, its
thresholds, and its recurring report. Agents do not read each other's raw data; they
exchange conclusions through the CEO. This keeps the prompts small and stops a change
in the finance schema from breaking the health agent.

The one deliberate exception is the **calendar**, which every agent reads. Time is the
universal currency, and an agent that cannot see your week will confidently recommend
things into a day that is already full.

## Failure modes designed against

**Silent staleness.** An agent reporting on a feed that stopped updating three weeks ago
is worse than no agent. Every specialist checks the freshness of its inputs first and
leads its report with a staleness warning if data is older than its expected cadence.

**Fabricated precision.** Agents state the confidence and the source of a number. "Your
spend is up 12%" is only useful alongside "based on 3 of 4 accounts; the credit card
feed hasn't synced since the 9th."

**The nag spiral.** A system that generates twenty recommendations a week trains you to
ignore it. Each specialist is capped at three actionable items per report, ranked. If
something is item four, it was not important enough this week.

**Profile drift.** Targets set in January are frequently wrong by June and nobody
notices, so the quarterly re-plan explicitly re-opens `profile.yaml` rather than
treating it as settled.
