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

The instinct to reach for Zapier first is worth resisting. Most of what people build in
Zapier for a system like this is now a connector call.

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
| Smart scale (Withings) | Withings Health API — proper OAuth, historical backfill | Notion `Body` DB | M |
| Smart scale (Renpho/other) | App → Apple Health/Google Fit → bridge app → webhook | Same | M |
| Apple Health aggregate | Health Auto Export (iOS) → scheduled webhook → Make → store | Notion / Sheet | M |
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
