#!/usr/bin/env bash
# Nightly GoAccess report for /var/www/learnche.org/_stats/index.html.
#
# Designed to be invoked from cron. Atomic write: builds to a .tmp file
# and renames into place so the public dashboard never serves a partial
# file.
#
# The production webserver is Caddy, whose default access log is JSON
# (one object per line). GoAccess does not understand Caddy JSON
# natively, so we pipe through scripts/server/caddy-json-to-combined.py
# which converts JSON lines to Apache combined format and passes any
# already-combined lines (e.g. archived pre-Hetzner Apache logs) through
# unchanged. The unioned stream is then fed to goaccess as combined.
#
# Configuration is read from /etc/pid-book/goaccessrc by default
# (see scripts/server/goaccessrc.example for a template).

set -euo pipefail

# --------------------------------------------------------------------------
# Configurable paths. Override via environment variables when invoking.
# --------------------------------------------------------------------------

LOG_GLOBS_DEFAULT=(
    # Caddy's default per-host access log on Debian/Ubuntu installs
    # (the path you use depends on the Caddyfile `output file` directive;
    #  see docs/telemetry/server-runbook.md).
    "/var/log/caddy/learnche.org.access.log*"
    # Archived pre-Hetzner Apache logs (combined format; passed through).
    "/var/log/learnche-archive/access.log*"
)

LOG_GLOBS=("${LOG_GLOBS:-${LOG_GLOBS_DEFAULT[*]}}")
GOACCESS_CONF="${GOACCESS_CONF:-/etc/pid-book/goaccessrc}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/www/learnche.org/_stats}"
OUTPUT_FILE="${OUTPUT_FILE:-${OUTPUT_DIR}/index.html}"

# Same-directory companion script that turns Caddy JSON into combined.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_TO_COMBINED="${JSON_TO_COMBINED:-${SCRIPT_DIR}/caddy-json-to-combined.py}"

# --------------------------------------------------------------------------
# Sanity checks.
# --------------------------------------------------------------------------

if ! command -v goaccess >/dev/null 2>&1; then
    echo "run-goaccess: goaccess not on PATH" >&2
    exit 2
fi
if [[ ! -x "${JSON_TO_COMBINED}" ]]; then
    echo "run-goaccess: ${JSON_TO_COMBINED} missing or not executable" >&2
    exit 2
fi

mkdir -p "${OUTPUT_DIR}"

CONF_FLAG=()
if [[ -f "${GOACCESS_CONF}" ]]; then
    CONF_FLAG=(--config-file="${GOACCESS_CONF}")
fi

# Expand globs ourselves so we can pass them to zcat.
shopt -s nullglob
log_files=()
for pattern in ${LOG_GLOBS[*]}; do
    for f in $pattern; do
        log_files+=("$f")
    done
done
shopt -u nullglob

if [[ ${#log_files[@]} -eq 0 ]]; then
    echo "run-goaccess: no log files matched: ${LOG_GLOBS[*]}" >&2
    exit 3
fi

TMP="$(mktemp -p "${OUTPUT_DIR}" .index.html.XXXXXX)"
trap 'rm -f "${TMP}"' EXIT

# --------------------------------------------------------------------------
# Run.
#
# zcat -f handles both plain and .gz files. The JSON filter passes
# combined-format lines through unchanged, so a mixed stream is fine.
# Bot, static-asset and panel filters live in goaccessrc.
# --------------------------------------------------------------------------

zcat -f "${log_files[@]}" |
    "${JSON_TO_COMBINED}" |
    goaccess - \
        "${CONF_FLAG[@]}" \
        --log-format=COMBINED \
        --no-global-config \
        --ignore-crawlers \
        --anonymize-ip \
        --4xx-to-unique-count \
        --html-report-title='learnche.org/pid — readership' \
        --output="${TMP}"

# Move into place atomically. mv on the same filesystem is atomic,
# so HTTP clients never see a half-written file.
chmod 0644 "${TMP}"
mv -f "${TMP}" "${OUTPUT_FILE}"
trap - EXIT

echo "run-goaccess: wrote ${OUTPUT_FILE} ($(wc -c <"${OUTPUT_FILE}") bytes)"
