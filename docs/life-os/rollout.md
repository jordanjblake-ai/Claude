# Phase 3 — Rollout

Sequenced so that something works within a week. The ordering rule is **value ÷ setup
effort**, with one override: whatever Round 1 names as the 90-day priority jumps the
queue even if it's expensive, because a system that ignores your stated top priority
loses your trust before it earns it.

## Week 1 — Things that work today

No new accounts, no new hardware, no middleware. Everything here runs on connectors
that are already live.

1. **Subscription audit.** Agent sweeps Gmail for receipts and renewal notices, builds
   the subscription list, flags anything unused or auto-renewing above a threshold.
   Usually pays for the entire system's setup effort in the first run.
2. **Relationship ledger seeded.** People, rings and cadence targets from Round 6 into
   Notion; birthdays confirmed against Contacts and written to Calendar with the lead
   time from Round 7.
3. **Calendar adherence baseline.** Two weeks of history read, categorised, and compared
   against where you *said* the time was going. This is uncomfortable and it is the most
   informative single output of the first week.
4. **Daily brief v1.** One screen, assembled from calendar, relationship nudges and
   goal deadlines. Deliberately thin — it earns more inputs by being read.

## Week 2–3 — The body

5. **Scale pipe.** Depends on the Round 5 answer. Withings is a clean API day; anything
   app-only routes through Apple Health plus a bridge app.
6. **Weight trend, not weight.** A 7-day moving average with a trend call. Daily weight
   is mostly water and it makes people quit; the trend is the only number the coach
   reports.
7. **Training adherence.** Planned sessions vs. calendar reality, with the failure
   pattern from Round 4 specifically watched for.

## Week 3–4 — The money

8. **Aggregator connected** (region-appropriate, per Round 3), or the CSV-to-Drive
   fallback if the aggregator is unavailable or overpriced in your market.
9. **Categorisation** into the 8–12 buckets from Round 3, with the agent proposing the
   bucket map from your actual transaction history rather than you inventing it upfront.
10. **Monthly close.** Net worth snapshot, spend vs. plan, and the one number from
    Round 2 tracked against its target.

## Week 4–5 — Signal and goals

11. **AI scout feeds** wired, filter calibrated against Round 8. Expect two or three
    rounds of "too much / wrong kind" before the filter is right. That tuning is normal
    and worth doing rather than tolerating a noisy digest.
12. **Goal ledger** seeded, with time-spent derived from tagged calendar blocks.
13. **Weekly review assembled** — all five specialists reporting into a CEO synthesis.
    This is the moment the system stops being five tools and starts being one.

## Week 6 onward — Compounding

14. **Gift concierge** goes proactive: running idea lists per person, lead-time alerts
    ahead of occasions.
15. **Arbitration live.** The CEO agent starts surfacing genuine cross-domain trade-offs
    rather than five parallel reports.
16. **Quarterly re-plan** scheduled, which re-opens `profile.yaml` itself.

## What to resist

**Building all five verticals at once.** The temptation is real because the architecture
is symmetric. But five half-wired pipes produce five stale reports, and staleness is the
failure mode that kills trust fastest.

**Perfect categorisation before any categorisation.** The bucket map will be wrong and
you'll fix it in week two from real data. Starting is cheaper than designing.

**Buying hardware before Round 5.** A wearable purchased to feed a system that turns out
not to need recovery data is an expensive way to add a charging cable to your life.

**Automating a decision you haven't made yet.** Automation locks in a policy. If you
don't yet know your cadence for second-ring friends, an automated nudge just generates
guilt on a schedule.
