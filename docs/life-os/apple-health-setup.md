# Apple Health → Life OS

There's no Apple Health connector in this environment, and there can't
really be one directly — Health data lives in a sandboxed store on your
iPhone, not behind any cloud API Apple exposes to third parties. A bridge
app or shortcut is the only way out. This is a setup guide for the phone,
not something Claude can do remotely.

## What it needs to do

Same pattern as everything else in this system: produce a file, drop it
somewhere Claude can read it. Concretely: export to CSV, save it into the
**"Life OS — Health Exports"** Drive folder (same one the Withings script
uses).

## Two free routes (revised — Health Auto Export's free tier doesn't
actually cover this)

Checked what's genuinely free as of August 2026: Health Auto Export's free
tier is widgets only — real CSV export needs its paid "Basic" tier, and
automated Google Drive export needs paid "Premium." So it's dropped as the
default recommendation. Two free alternatives instead:

### Option A — Simple Health Export CSV (recommended starting point)

A free app (tip-supported, not paywalled) that exports your full Health
data to CSV in one tap.

1. Install **Simple Health Export CSV** from the App Store.
2. Install the **Google Drive app** if it isn't already on your phone, and
   sign in with the same Google account this Life OS uses
   (`jordanjblake@gmail.com`) — this is what lets iOS's share sheet see
   Drive as a save destination.
3. Open the app, export, then use the share sheet to **save the CSV
   directly to the "Life OS — Health Exports" Drive folder**.
4. This is manual-trigger, not scheduled — run it whenever you want fresh
   data pulled in. That's fine: the health-coach reports trends, not single
   readings, so occasional manual exports are enough, and it matches how
   the Withings script already works.

### Option B — Build it yourself with Apple's native Shortcuts app (fully
automated, still free)

More setup effort, but genuinely free and unlimited — no app purchase at
all. The Health app exposes "Health Sample" actions directly to Shortcuts
(built into iOS):

1. In the **Shortcuts** app, create a new shortcut.
2. Add a **"Get Health Samples"** action for each metric that matters —
   weight, body fat %, resting heart rate, sleep analysis, and anything
   Eight Sleep writes into Health (worth checking whether it does; if so,
   this is also how sleep stages/HRV reach the Life OS).
3. Add a **"Save File"** action, pointed at the "Life OS — Health Exports"
   Drive folder (via the Files integration from step 2 above).
4. Add a **Personal Automation** (Automation tab → "+") to run this
   shortcut on a schedule — a time-of-day trigger is free, no subscription
   needed.

Worth doing once Option A proves the pipeline works end-to-end and you want
it fully hands-off.

## What Claude does from here

Once a CSV lands in that Drive folder, treat it the same way as the
LifeStage exports and the Withings CSVs — read, parse, and write the
relevant fields into the Notion `Body` database. No separate ingestion path
needed; all three sources funnel into the same folder and the same read
step.

## Status

Not yet done — this is the setup guide, not a confirmation it's been set
up. Come back and update `profile/profile.yaml → health.sensors` once it's
live.
