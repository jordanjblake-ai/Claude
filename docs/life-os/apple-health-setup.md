# Apple Health → Life OS

There's no Apple Health connector in this environment, and there can't
really be one directly — Health data lives in a sandboxed store on your
iPhone, not behind any cloud API Apple exposes to third parties. The
standard bridge is a third-party export app; **Health Auto Export** is the
one with the best reputation for this. This is a setup guide for the phone,
not something Claude can do remotely.

## What it needs to do

Same pattern as everything else in this system: produce a file, drop it
somewhere Claude can read it. Concretely: export to CSV, save it into the
**"Life OS — Health Exports"** Drive folder (same one the Withings script
uses), on a schedule.

## Setup steps (on your iPhone)

1. **Install Health Auto Export** from the App Store (the free tier covers
   CSV export; the automation/scheduling features are a paid tier — worth it
   if you want this hands-off rather than manual).

2. **Install the Google Drive app** if it isn't already on your phone, and
   sign in with the same Google account this Life OS uses
   (`jordanjblake@gmail.com`). This matters because it's what lets iOS's
   Files app "Save to..." picker see Drive as a destination.

3. **In Health Auto Export, create an export** for the metrics that matter
   to the health-coach — at minimum: weight, body fat %, resting heart rate,
   sleep analysis, and anything Eight Sleep is writing into Health (check
   whether it does — if Eight Sleep pushes sleep stages/HRV into Apple
   Health, this is also how that data reaches the Life OS).

4. **Set the export format to CSV.**

5. **Set the destination.** Depending on the app version, this is either:
   - A direct **"Automations"** feature that can export on a schedule to a
     folder — if it offers Google Drive natively, use that.
   - Or, more commonly, an **iOS Shortcut**: Health Auto Export has a
     Shortcuts action ("Export Health Data") you can chain to a "Save File"
     action, and point that Save File action at Drive (via the Files app
     integration from step 2).

   Whichever path is available in your version of the app, the destination
   folder is **"Life OS — Health Exports."**

6. **Schedule it**, if you have the paid tier — daily or weekly is both
   fine, the health-coach reports trends, not single readings, so it
   doesn't need to be frequent. Without the paid tier, run the export
   manually whenever you want fresh data pulled in, same as the Withings
   script.

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
