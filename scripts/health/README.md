# Withings sync — setup

`withings_sync.py` runs on your own machine (Windows laptop), not in the
Claude Code cloud session — OAuth needs a browser redirect back to
`localhost`, which only your machine can catch. Its output is a CSV you drop
into Drive, the same pattern already working for the LifeStage Money
exports.

Standard library only. Any Python 3 install works — no `pip install` needed.

## One-time setup

1. **Register an app with Withings.**
   Go to <https://developer.withings.com>, sign in with your Withings
   account, and create a new application. Use these exact values:
   - **Callback URL / Redirect URI:** `http://localhost:8085/callback`
   - Everything else (name, description) can be whatever you like — e.g.
     "Life OS Sync".

   This gives you a **Client ID** and **Client Secret**. Treat the secret
   like a password — it does not go in this repo, in Slack, or anywhere
   else committed to git.

2. **Set them as environment variables**, not in any file:

   PowerShell:
   ```powershell
   $env:WITHINGS_CLIENT_ID = "your-client-id"
   $env:WITHINGS_CLIENT_SECRET = "your-client-secret"
   ```

   These only last for the current terminal session. If you want them to
   persist, use Windows' "Edit environment variables for your account"
   settings instead of typing the secret into a script.

3. **Authorize once:**
   ```
   python3 withings_sync.py auth
   ```
   This opens your browser to a Withings consent screen. Approve it. The
   script catches the redirect on `localhost:8085` and saves tokens to
   `.withings_tokens.json` in this folder — that file is git-ignored, it
   will never get committed.

## Ongoing use

```
python3 withings_sync.py sync
```

Fetches the last 30 days of weight and body-composition measurements
(weight, fat %, fat mass, muscle mass, hydration, bone mass) and writes a
CSV into `scripts/health/exports/` (also git-ignored). Use `--days N` for a
different window, e.g. `--days 90` the first time to backfill more history.

**Then move the CSV into the "Life OS — Health Exports" Drive folder** —
that's the handoff point. From there, the Life OS session reads and parses
it the same way it already does for LifeStage exports.

Run `sync` however often you want fresh data pulled — there's nothing
scheduled automatically yet. A Windows Task Scheduler job pointed at this
command is the natural next step if you want it hands-off, but that's a
separate decision, not set up by default.

## If something breaks

The measurement type codes and endpoint URLs in `withings_sync.py` reflect
Withings' public API as documented for years, but they weren't re-verified
against the live docs at build time (this session's network access to
`developer.withings.com` was blocked). If `auth` or `sync` fails with an API
error, check <https://developer.withings.com/api-reference/> for anything
that's changed.
