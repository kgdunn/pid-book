#!/usr/bin/env bash
# Alert when the public stats artifact has gone stale.
#
# The /pid/stats dashboard and the sidebar sparklines render whatever is
# in sparklines.json; they anchor their display window to the newest date
# in that file. So when the nightly builder stops writing a fresh file,
# the dashboard does not error: it silently freezes on the last good day.
# That failure mode once went unnoticed for ~10 days.
#
# This guard makes the freeze loud. Run it from cron straight after the
# nightly build. On a fresh file it prints one OK line to stdout; on a
# missing or stale file it prints to *stderr* and exits non-zero, so a
# cron MAILTO mails it (keep the check's stderr OUT of the >> log
# redirect in the cron line, or cron sees no output and stays silent).
#
# Usage:
#   check-stats-fresh.sh [TARGET]
# Environment:
#   MAX_AGE_HOURS  staleness threshold in hours (default 26 = nightly
#                  cadence plus a few hours of slack).

set -euo pipefail

TARGET="${1:-/var/www/learnche.org/_stats/sparklines.json}"
MAX_AGE_HOURS="${MAX_AGE_HOURS:-26}"

if [[ ! -f "${TARGET}" ]]; then
    echo "check-stats-fresh: MISSING ${TARGET}" >&2
    exit 1
fi

now="$(date +%s)"
mtime="$(stat -c %Y "${TARGET}")"
age_h=$(( (now - mtime) / 3600 ))

if (( age_h > MAX_AGE_HOURS )); then
    echo "check-stats-fresh: STALE ${TARGET} is ${age_h}h old (> ${MAX_AGE_HOURS}h); the nightly builder is not writing it." >&2
    exit 1
fi

echo "check-stats-fresh: OK ${TARGET} is ${age_h}h old"
