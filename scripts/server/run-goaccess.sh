#!/usr/bin/env bash
# Nightly GoAccess report for /var/www/learnche.org/_stats/index.html.
#
# Designed to be invoked from cron. Stages the HTML in /tmp first
# (so goaccess writes can't bump into permissions or AppArmor on the
# /var/www/ path), then moves into place.
#
# The pipeline pipes log input through caddy-json-to-combined.py, which
# converts Caddy JSON lines to Apache combined format and passes
# already-combined lines (Apache logs) through unchanged. Both formats
# in the same input stream are fine.
#
# Configuration:
#   * /etc/pid-book/goaccessrc is loaded if present (see
#     scripts/server/goaccessrc.example for a template; the example is
#     known compatible with GoAccess 1.4 — the Debian 11 version).
#   * LOG_GLOBS env var overrides the default log paths. Set this for
#     Apache servers; the default below tries Caddy first, Apache
#     second.
#
# Known GoAccess 1.4 gotchas the wrapper accounts for:
#   1. --output=<path> rejects any path whose final extension is not
#      .html/.csv/.json. We use mktemp --suffix=.html for that reason.
#   2. --anonymize-ip was added in 1.6; passing it on 1.4 is silently
#      accepted but causes 0-byte output. Omitted here.
#   3. goaccess errors during HTML generation may be printed only to
#      stderr; the wrapper redirects stderr into the pipeline so cron
#      mail and /var/log/pid-book-stats.log catch them.

set -euo pipefail

# --------------------------------------------------------------------------
# Configurable paths. Override via environment variables when invoking.
# --------------------------------------------------------------------------

LOG_GLOBS_DEFAULT=(
    # Try common Caddy / Apache / Nginx default per-host log locations.
    # If your server is elsewhere, set LOG_GLOBS in the cron file or the
    # `logs =` line of sparklines.conf (read below).
    "/var/log/caddy/learnche.org.access.log*"
    "/var/www/logs/learnche.org/access.log*"
    "/var/log/apache2/learnche.org-access.log*"
    "/var/log/nginx/learnche.org.access.log*"
    "/var/log/learnche-archive/access.log*"
)

# Single source of truth for the log path. Precedence:
#   1. LOG_GLOBS in the environment (highest; set by cron for one-offs).
#   2. The `logs =` line in sparklines.conf, so this script and
#      build-sparklines.py read the *same* paths and cannot drift apart.
#      (Drift is exactly what silently froze the dashboard once: the
#      builder config pointed at the live Apache log while this script's
#      cron override still pointed at the not-yet-existent Caddy path.)
#   3. The built-in default list above.
SPARKLINES_CONF="${SPARKLINES_CONF:-/etc/pid-book/sparklines.conf}"
if [[ -z "${LOG_GLOBS:-}" && -f "${SPARKLINES_CONF}" ]] && command -v python3 >/dev/null 2>&1; then
    conf_logs="$(python3 - "${SPARKLINES_CONF}" <<'PY'
import configparser, sys
cfg = configparser.ConfigParser()
cfg.read(sys.argv[1])
print(cfg.get("paths", "logs", fallback="").strip())
PY
)"
    [[ -n "${conf_logs}" ]] && LOG_GLOBS="${conf_logs}"
fi

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

# Stage in /tmp first. Two reasons:
#   (a) some goaccess builds (and AppArmor profiles) refuse writes
#       outside /tmp when running as root.
#   (b) mktemp --suffix=.html ensures the output filename ends in
#       .html, which goaccess 1.4 requires.
TMP="$(mktemp --suffix=.html /tmp/run-goaccess.XXXXXX)"
trap 'rm -f "${TMP}"' EXIT

# --------------------------------------------------------------------------
# Run. stderr is merged into stdout so any goaccess errors land in the
# same place cron's MAILTO / journal logs already capture.
# --------------------------------------------------------------------------

zcat -f "${log_files[@]}" |
    "${JSON_TO_COMBINED}" |
    goaccess - \
        "${CONF_FLAG[@]}" \
        --log-format=COMBINED \
        --no-global-config \
        --ignore-crawlers \
        --4xx-to-unique-count \
        --html-report-title='learnche.org/pid readership' \
        --output="${TMP}" 2>&1

# Sanity check: goaccess sometimes returns 0 even after a write error.
# Refuse to publish a zero-byte report — leaves the previous good one
# in place.
if [[ ! -s "${TMP}" ]]; then
    echo "run-goaccess: goaccess produced zero bytes; not publishing." >&2
    exit 4
fi

chmod 0644 "${TMP}"
mv -f "${TMP}" "${OUTPUT_FILE}"
trap - EXIT

echo "run-goaccess: wrote ${OUTPUT_FILE} ($(wc -c <"${OUTPUT_FILE}") bytes)"
