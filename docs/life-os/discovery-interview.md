# Phase 1 — Discovery & Diagnostics

The interview runs in **rounds of 3–4 questions**. Answer a round, the answers get
written into `profile/profile.yaml`, the round gets ticked here, and the next round
opens. Skipping a round is fine; the agent that depended on it will simply tell you it
is missing that input rather than guessing.

Answering is not homework. Every question below exists because some agent cannot act
without it — the "unlocks" line says which one.

## Progress

- [ ] Round 1 — Orientation (cross-cutting)
- [ ] Round 2 — Finance: the picture
- [ ] Round 3 — Finance: the plumbing
- [ ] Round 4 — Health: the target
- [ ] Round 5 — Health: the sensors
- [ ] Round 6 — Relationships: the people
- [ ] Round 7 — Relationships: the occasions
- [ ] Round 8 — AI stack: what you're tracking and why
- [ ] Round 9 — Hobbies & goals
- [ ] Round 10 — Cadence, surfaces and guardrails

---

## Round 1 — Orientation

The only round that is genuinely mandatory. It sets priority ranking, which is what the
CEO agent uses to arbitrate every later conflict.

1. **If this system only fixed one thing in the next 90 days, what would it be?** Name
   the outcome, not the tool — "know exactly where my money goes without thinking about
   it", not "a spending dashboard".
   *Unlocks: build sequencing. Everything else queues behind this.*

2. **Rank the five verticals** — Personal Finance, Health & Fitness, Relationships, AI
   Innovation, Hobbies/Goals — from most to least important **right now**. Ties are not
   allowed; a tie means the CEO agent escalates a decision to you that it could have
   made itself.
   *Unlocks: arbitration rule 1. Without this the CEO agent has no way to resolve
   conflicts between specialists.*

3. **Where does the current system leak?** What did you intend to do in the last month
   that quietly didn't happen — a missed payment, a skipped block of training, a friend
   you meant to call, a paper you meant to read?
   *Unlocks: the quick-win list. Leaks are where automation pays back fastest.*

4. **What's your stack and your country?** Phone (iOS/Android), watch or wearable, smart
   scale, where notes and tasks live today (Notion/Obsidian/Apple Notes/nothing), and
   which country you bank in.
   *Unlocks: essentially all of Phase 2. Bank aggregation and health APIs are both
   region-locked, so the country answer changes the entire finance pipeline.*

---

## Round 2 — Finance: the picture

1. What are your income sources, and are any of them variable or lumpy (contracting,
   bonus, dividends, side income)?
2. What is the single financial number you most want to move, and to what, by when?
   Net worth, savings rate, debt balance, runway, monthly spend — one number.
3. What are the fixed commitments that must never be missed? Mortgage/rent, loans,
   insurance, tax instalments.
4. What's the honest state of debt — balances, rates, and whether any of it is
   revolving credit-card debt?

## Round 3 — Finance: the plumbing

1. Which banks and cards, and do you already use an aggregator (Plaid, TrueLayer,
   Basiq, Akahu, Monarch, YNAB, Copilot)?
2. Are there investment/pension accounts that need to appear in net worth, and do they
   expose an API or only a monthly statement?
3. How do you want spending categorised — a handful of buckets you'll actually read, or
   granular categories? (Recommendation: 8–12 buckets. Granularity you don't act on is
   just data entry with extra steps.)
4. Do you want the CFO agent to have write access anywhere (moving money, paying cards),
   or is it strictly read-and-report? (Recommendation: read-only until you've watched it
   be right for a full quarter.)

## Round 4 — Health: the target

1. What's the actual objective — fat loss, strength, endurance, body recomposition,
   longevity markers, or simply consistency?
2. Current and target: weight, and any other number you care about (body fat, a lift, a
   race time, resting heart rate).
3. What does a realistic training week look like — how many sessions, what type, and
   what time of day do they have to happen to survive contact with your calendar?
4. What has derailed training before? Injury, travel, work crunch, motivation, or
   childcare — the coach agent should be watching for your specific failure pattern, not
   a generic one.

## Round 5 — Health: the sensors

1. Smart scale — make and model? (Withings and Renpho both have workable paths; some
   budget scales are app-only dead ends, which changes the recommendation.)
2. Wearable — Apple Watch, Garmin, Whoop, Oura, Fitbit, none? Each has a different
   export story and this determines whether sleep and recovery are in scope at all.
3. Do you track nutrition, and if so where (MyFitnessPal, Cronometer, nothing)? Honest
   answer preferred — if the real answer is "I've tried three times and stopped", the
   system should not be built on it.
4. Apple Health or Google Fit as the aggregation hub, and are you willing to install one
   bridge app (e.g. Health Auto Export) to get data out of it?

## Round 6 — Relationships: the people

1. Who's in the inner circle — partner, family, closest friends — the people where a
   month of silence is a problem?
2. Who's in the second ring: friends and colleagues worth a quarterly check-in, where
   drift happens without anyone noticing?
3. What cadence feels right for each ring, and would you rather the agent prompt you to
   reach out, or draft the message for you to send?
4. Are there relationships that need active repair or deliberate investment right now?

## Round 7 — Relationships: the occasions

1. Birthdays and anniversaries — are they already in a calendar or contacts app, or
   scattered in your head?
2. What's your gifting philosophy and typical budget by ring? The gift concierge needs
   a range and a taste, otherwise it recommends candles.
3. How far ahead do you want warning — enough to order something thoughtful, or enough
   to plan a trip?
4. Any standing commitments the system should protect on the calendar — date night,
   a weekly family call, a regular dinner?

## Round 8 — AI stack: what you're tracking and why

1. Are you tracking AI professionally, personally, or both — and what decision does the
   tracking feed? (Building products, investing, career positioning, curiosity — each
   implies a completely different filter.)
2. Which sources do you already trust? Specific labs, researchers, newsletters,
   podcasts, subreddits, arXiv categories.
3. What's your current AI toolchain — Claude, Cursor, Copilot, local models, agent
   frameworks — and what have you been meaning to evaluate but haven't?
4. Digest cadence and depth: daily headlines, or a weekly brief that only surfaces
   things that change what you'd actually do?

## Round 9 — Hobbies & goals

1. What are the active hobbies, and which one has been starved of time longest?
2. Any long-horizon goals with a real deadline — a race, a trip, a launch, a
   qualification, a build?
3. What's a skill you want to be measurably better at in twelve months, and is there a
   way to measure it?
4. How much genuinely uncommitted time exists in a normal week? (Be pessimistic. Plans
   built on optimistic time budgets are the single most common reason goal systems
   collapse.)

## Round 10 — Cadence, surfaces and guardrails

1. When and where do you want the daily brief — time of day, and delivered as an email,
   a Notion page, or waiting for you when you open Claude?
2. Which day and time for the weekly review, and how long are you willing to spend on it?
3. What should the system never do without asking — send messages as you, spend money,
   write to your calendar, contact people directly?
4. What's the tone you want when you're off-track: blunt, or gentle? The system will do
   either, but it needs to be told, because the default of "blunt" is wrong for a
   meaningful number of people.
