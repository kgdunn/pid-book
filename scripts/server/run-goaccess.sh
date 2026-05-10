#!/usr/bin/env bash
# Nightly GoAccess report for /var/www/learnche.org/_stats/index.html.
#
# Designed to be invoked from cron. Atomic write: builds to a .tmp file
# and renames into place so the public dashboard never serves a partial
# file.
#
# Configuration is read from /etc/pid-book/goaccessrc by default
# (see scripts/server/goaccessrc.example for a template).

set -euo pipefail

# --------------------------------------------------------------------------
# Configurable paths. Override via environment variables when invoking.
# --------------------------------------------------------------------------

LOG_GLOBS_DEFAULT=(
    "/var/log/nginx/learnche.org.access.log*"
    "/var/log/learnche-archive/access.log*"
)

LOG_GLOBS=("${LOG_GLOBS:-${LOG_GLOBS_DEFAULT[*]}}")
GOACCESS_CONF="${GOACCESS_CONF:-/etc/pid-book/goaccessrc}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/www/learnche.org/_stats}"
OUTPUT_FILE="${OUTPUT_FILE:-${OUTPUT_DIR}/index.html}"

# --------------------------------------------------------------------------
# Sanity checks.
# --------------------------------------------------------------------------

if ! command -v goaccess >/dev/null 2>&1; then
    echo "run-goaccess: goaccess not on PATH" >&2
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
# zcat -f handles both plain and .gz files. The bot, static-asset and
# panel filters live in goaccessrc. Anything passed here is a default
# the conf can override.
# --------------------------------------------------------------------------

zcat -f "${log_files[@]}" |
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
