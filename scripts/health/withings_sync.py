#!/usr/bin/env python3
"""
Withings sync for the Life OS.

Runs LOCALLY on the owner's machine -- this repo's Claude Code session has
no way to complete an OAuth browser redirect or reach a device-local API, so
this script is the piece that has to run outside the cloud session. Its only
job is to turn Withings measurements into a CSV, matching the same pattern
already working for LifeStage Money exports: a local script/app produces a
file, the owner drops it into a Drive folder, and the Life OS reads it from
there. No new integration style, same one reused.

Standard library only -- no pip install required.

Setup (one-time, see scripts/health/README.md for the full walkthrough):
    1. Register an application at https://developer.withings.com to get a
       Client ID and Client Secret.
    2. Set them as environment variables (never hardcode, never commit):
           export WITHINGS_CLIENT_ID=...
           export WITHINGS_CLIENT_SECRET=...
    3. Run:  python3 withings_sync.py auth
       This opens your browser, you approve access, and this script catches
       the redirect on localhost and stores tokens in .withings_tokens.json
       (gitignored -- never committed).

Ongoing use:
    python3 withings_sync.py sync [--days N]
       Fetches the last N days (default 30) of weight/body-composition
       measurements and writes a CSV into scripts/health/exports/ (also
       gitignored). Move that CSV into the "Life OS -- Health Exports" Drive
       folder and the Life OS session picks it up from there.

The measurement type codes and endpoint shapes below reflect Withings' public
API as it has been stable for years, but this session could not reach
developer.withings.com directly to re-verify at build time (network egress
to that domain was blocked). If `auth` or `sync` fails with an API error,
check https://developer.withings.com/api-reference/ for anything that's
since changed and adjust MEASURE_TYPES / the endpoint constants below.
"""

import csv
import http.server
import json
import os
import sys
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path

AUTHORIZE_URL = "https://account.withings.com/oauth2_user/authorize2"
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
MEASURE_URL = "https://wbsapi.withings.net/measure"
REDIRECT_URI = "http://localhost:8085/callback"
SCOPE = "user.metrics"

# Withings measurement type codes we care about for the health-coach.
# value in the API response is an integer that must be multiplied by
# 10 ** unit to get the real number (e.g. value=857, unit=-1 -> 85.7).
MEASURE_TYPES = {
    1: "weight_kg",
    6: "fat_ratio_pct",
    8: "fat_mass_kg",
    76: "muscle_mass_kg",
    77: "hydration_kg",
    88: "bone_mass_kg",
}

HERE = Path(__file__).resolve().parent
TOKENS_FILE = HERE / ".withings_tokens.json"
EXPORTS_DIR = HERE / "exports"


def _client_credentials():
    client_id = os.environ.get("WITHINGS_CLIENT_ID")
    client_secret = os.environ.get("WITHINGS_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(
            "Set WITHINGS_CLIENT_ID and WITHINGS_CLIENT_SECRET as environment "
            "variables first -- see scripts/health/README.md."
        )
    return client_id, client_secret


def _post_form(url, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    if body.get("status") != 0:
        sys.exit(f"Withings API error (status {body.get('status')}): {body}")
    return body["body"]


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            _CallbackHandler.code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Authorized. You can close this tab and return to the terminal.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No authorization code received.")

    def log_message(self, *args):
        pass  # keep the terminal quiet


def cmd_auth():
    client_id, client_secret = _client_credentials()

    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "state": "life-os-withings-auth",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
    }
    url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(auth_params)}"
    print("Opening your browser to authorize this app with Withings...")
    print(f"If it doesn't open automatically, visit:\n  {url}\n")
    webbrowser.open(url)

    server = http.server.HTTPServer(("localhost", 8085), _CallbackHandler)
    print("Waiting for the redirect back to localhost:8085 ...")
    server.handle_request()  # blocks for exactly one request, then returns

    code = _CallbackHandler.code
    if not code:
        sys.exit("Did not receive an authorization code. Try again.")

    token_body = _post_form(
        TOKEN_URL,
        {
            "action": "requesttoken",
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )

    TOKENS_FILE.write_text(json.dumps(token_body, indent=2))
    print(f"Authorized. Tokens saved to {TOKENS_FILE} (not committed to git).")


def _refresh_tokens():
    if not TOKENS_FILE.exists():
        sys.exit("No tokens found -- run `python3 withings_sync.py auth` first.")
    tokens = json.loads(TOKENS_FILE.read_text())
    client_id, client_secret = _client_credentials()

    token_body = _post_form(
        TOKEN_URL,
        {
            "action": "requesttoken",
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": tokens["refresh_token"],
        },
    )
    TOKENS_FILE.write_text(json.dumps(token_body, indent=2))
    return token_body["access_token"]


def cmd_sync(days):
    access_token = _refresh_tokens()  # refresh tokens are one-time use; rotate every run

    start = datetime.now(timezone.utc) - timedelta(days=days)
    params = {
        "action": "getmeas",
        "meastypes": ",".join(str(t) for t in MEASURE_TYPES),
        "category": "1",  # real measures, not user-declared objectives
        "startdate": str(int(start.timestamp())),
        "enddate": str(int(datetime.now(timezone.utc).timestamp())),
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        MEASURE_URL,
        data=data,
        method="POST",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    if body.get("status") != 0:
        sys.exit(f"Withings API error (status {body.get('status')}): {body}")

    groups = body["body"].get("measuregrps", [])
    if not groups:
        print(f"No measurements found in the last {days} days.")
        return

    EXPORTS_DIR.mkdir(exist_ok=True)
    out_path = EXPORTS_DIR / f"withings_export_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv"

    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date"] + list(MEASURE_TYPES.values()))
        for group in sorted(groups, key=lambda g: g["date"]):
            row = {name: "" for name in MEASURE_TYPES.values()}
            for m in group["measures"]:
                name = MEASURE_TYPES.get(m["type"])
                if name:
                    row[name] = m["value"] * (10 ** m["unit"])
            date_str = datetime.fromtimestamp(group["date"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            writer.writerow([date_str] + [row[name] for name in MEASURE_TYPES.values()])

    print(f"Wrote {len(groups)} measurement(s) to {out_path}")
    print('Move this file into the "Life OS -- Health Exports" Drive folder so the Life OS session can read it.')


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("auth", "sync"):
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "auth":
        cmd_auth()
    else:
        days = 30
        if "--days" in sys.argv:
            days = int(sys.argv[sys.argv.index("--days") + 1])
        cmd_sync(days)


if __name__ == "__main__":
    main()
