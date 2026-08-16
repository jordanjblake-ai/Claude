# Phase 2 — Data & Tool Map

Every row below is a pipe: a source, the thing that reaches it, where the data lands,
and what it costs in setup effort. Effort is rated **S** (minutes), **M** (an evening),
**L** (a weekend, or a paid service).

Recommendations here are provisional until Round 1 of the interview establishes the
owner's country and hardware — bank aggregation and health data are both region-locked
and device-locked, and a recommendation made before those answers is a guess.

## Substrate decision

Three ways to move data. Use the cheapest one that works:

1. **Claude's own connectors** (already live: Gmail, Calendar, Drive, Notion, GitHub).
   Zero infrastructure, zero cost, no task quotas. Use for anything Claude can reach.
2. **Make.com** for everything else. Preferred over Zapier for this use case: multi-step
   scenarios are dramatically cheaper per operation, and this system is mostly
   many-steps-few-runs. n8n self-hosted is the alternative if you'd rather own it.
3. **A scheduled agent** for judgement calls. If a step requires reading something and
   deciding, that is not an automation step, it is an agent step.
4. **A local script + Drive drop**, for sources that need something only the owner's own
   device can do — an OAuth browser redirect to `localhost`, or reading a sandboxed store
   like Apple Health. The script's only job is producing a file; Drive (already live)
   is the handoff back into everything else. First used for the LifeStage Money CSV
   exports, now reused for Withings (`scripts/health/withings_sync.py`) and Apple Health
   (`docs/life-os/apple-health-setup.md`). Prefer this over inventing a new integration
   shape every time a source can't be reached directly from the cloud.

The instinct to reach for Zapier first is worth resisting. Most of what people build in
Zapier for a system like this is now a connector call.

### Candidate: a quick-capture channel (Telegram bot)

Not yet built. Surfaced by a real gap: the owner arranges things with people who aren't
in this system — his beach volleyball coach and his cleaner — over WhatsApp and Facebook
Messenger respectively, neither of which has a connector here, so an agent has no way to
know when a session or a visit happened.

For those two specific cases the fix doesn't need new infrastructure: the owner already
creates calendar events for both, so putting the missing detail (headcount, visit
confirmation) directly in the event title or description gives every agent a readable
signal with zero behaviour change asked of Mark or Justyna. That's the v1 approach — see
`profile.yaml → finance.payment_automation_requested`.

Telegram is worth naming separately because it's the strongest candidate **if** a
general-purpose capture channel is ever wanted — "log X" from a phone in two seconds,
for anything in the Life OS, not tied to one payee. Telegram's Bot API is free and needs
no business verification, unlike WhatsApp Business API or the Messenger Platform, both
of which require an approval process disproportionate to a personal system. The cost is
real, though: no connector exists for it yet, so it's a genuine build (a bot + a small
relay into Notion/the agents), not a flip of a switch — and it only helps for capture
*by the owner*; it doesn't retroactively give visibility into conversations happening on
other platforms. Revisit if/when a second or third case like Mark/Justyna shows up and
the per-case calendar workaround stops scaling.

## Personal Finance

| Source | Reach it with | Lands in | Effort |
| --- | --- | --- | --- |
| Bank & card transactions | Region-dependent aggregator — Plaid (US/CA/UK/EU), TrueLayer (UK/EU), Basiq or Up's API (AU), Akahu (NZ) | Notion `Transactions` DB or Sheet | L |
| Bank & card, no-API fallback | Monthly CSV export → Drive folder → agent parses | Same | M |
| Subscriptions & renewals | Gmail search for receipt/renewal patterns — **already live** | Notion `Subscriptions` DB | S |
| Investments & pension | Broker API where available; otherwise monthly statement PDF → Drive | Notion `Net Worth` DB | M |
| Net worth snapshot | Scheduled agent, monthly, reads the above | Notion, one row per month | S |

The Gmail-receipt pipe is the standout quick win: it needs no new accounts, no
credentials, and it typically finds real money. Subscription leakage is the most
reliably recoverable spend in a personal budget, and it's sitting in an inbox you
already granted access to.

The bank aggregator is the expensive item and the one to defer until Round 3. Consumer
aggregator pricing and coverage vary enough by country that picking one before knowing
the country wastes the setup effort.

## Health & Fitness

| Source | Reach it with | Lands in | Effort |
| --- | --- | --- | --- |
| Smart scale (Withings) | **BUILDING.** Withings Health API via OAuth — `scripts/health/withings_sync.py` in this repo (local script, own-device OAuth, outputs CSV) | Notion `Body` DB | M |
| Apple Health aggregate | **BUILDING.** Health Auto Export (iOS) → CSV → Drive folder (see `docs/life-os/apple-health-setup.md`) — simpler than the originally-planned webhook/Make route since Drive is already a live connector | Notion `Body` DB | M |
| Garmin / Whoop / Oura | Official developer APIs; Whoop and Oura are the friendliest | Notion `Recovery` DB | M |
| Google Fit | Fitness REST API | Sheet | M |
| Training sessions | Strava API, or calendar events tagged as training | Notion `Training` DB | S–M |
| Session adherence | Calendar API — **already live** | Derived, no storage | S |

Adherence via calendar is the sleeper quick win here. You don't need a wearable to
answer "did the training block survive the week" — you need the calendar you already
have, compared against the plan. That single comparison catches drift weeks before the
scale does.

A caution on scales: several budget brands are app-only with no export path and no
Apple Health write. If the scale is one of those, the honest recommendation is to
replace the hardware rather than build a fragile scraper around it.

## Relationship Management

| Source | Reach it with | Lands in | Effort |
| --- | --- | --- | --- |
| People & rings | Google Contacts, or hand-seeded once from Round 6 | Notion `People` DB | S |
| Birthdays & anniversaries | Contacts → Calendar recurring events — **already live** | Calendar | S |
| Last-contact signal | Gmail thread dates per person — **already live** | Derived onto `People` | S |
| Meeting/call history | Calendar attendee history — **already live** | Derived | S |
| Gift ideas | Agent-maintained running list per person | Notion `People` DB | S |
| Nudges | Scheduled agent compares cadence target vs. last contact | Daily brief | S |

This vertical is almost entirely buildable today with live connectors and no new
tooling. It is the highest ratio of value to setup effort in the whole system, which is
why it appears early in the rollout despite rarely being anyone's top-ranked priority.

One design note: last-contact inferred from email is a decent proxy and a poor truth.
It misses the phone calls and the in-person coffees, which are exactly the contacts that
matter most. Treat the derived signal as a prompt to confirm, never as a fact to report.

## AI Innovation Tracking

| Source | Reach it with | Lands in | Effort |
| --- | --- | --- | --- |
| arXiv (cs.AI, cs.CL, cs.LG) | arXiv API with keyword filter | Notion `Watchlist` | S |
| Lab announcements | RSS from Anthropic, OpenAI, DeepMind, Meta AI | Same | S |
| Newsletters you already get | Gmail label + agent digest — **already live** | Same | S |
| Model/API changelogs | Docs RSS or scheduled fetch | Same | S |
| GitHub releases & trending | GitHub API — **already live** | Same | S |
| Weekly digest | Scheduled agent filters, ranks, writes brief | Email or Notion | S |

The hard part is not collection, it is the filter. Raw AI feeds produce hundreds of
items a week and reading them is a full-time job that produces no decisions. Round 8
exists to establish what the tracking is *for*, because the filter is entirely
downstream of that answer. Without it, this agent produces a newsletter nobody reads —
including its owner.

## Hobbies & Goals

| Source | Reach it with | Lands in | Effort |
| --- | --- | --- | --- |
| Goal ledger | Seeded from Round 9, agent-maintained | Notion `Goals` DB | S |
| Time actually spent | Calendar blocks tagged by project — **already live** | Derived | S |
| Practice/session logs | Agent captures conversationally, not by form | Notion `Sessions` DB | S |
| Deadlines & milestones | Calendar — **already live** | Calendar | S |
| Spend against hobby budget | Inherited from the finance pipe, tagged | Derived | S |

That last row is where the quest-master and the CFO will argue, which is exactly what
the arbitration rules in `CLAUDE.md` exist to settle.

## Secrets

No credential, token, account number or API key goes in this repository. Store them in
the automation platform's vault (Make has one; n8n has credentials storage) and
reference them by name. The profile stores *which* accounts exist, never how to open
them.
