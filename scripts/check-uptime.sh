#!/usr/bin/env bash
set -euo pipefail

# The override also allows the check to be exercised against a local test server.
base_url="${SITE_URL:-https://sites-para-boas-ideias.vercel.app}"
base_url="${base_url%/}"
retries="${UPTIME_RETRIES:-2}"
retry_delay="${UPTIME_RETRY_DELAY:-3}"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

for path in / /index-7.html; do
  url="${base_url}${path}"
  response="${tmpdir}/response.html"
  rm -f "$response"
  status=""

  if ! status="$(curl --fail --silent --show-error --location \
    --retry "$retries" --retry-all-errors --retry-delay "$retry_delay" \
    --connect-timeout 10 --max-time 20 \
    --output "$response" --write-out '%{http_code}' -- "$url")"; then
    printf 'FAILED: %s could not be fetched (HTTP %s)\n' "$url" "${status:-unknown}" >&2
    exit 1
  fi

  if [[ "$status" != 200 ]] || \
    ! grep -Eqi '<html([[:space:]>]|$)' "$response" || \
    ! grep -Eqi 'Risco[[:space:]]+(&amp;|&)[[:space:]]+Rumo' "$response"; then
    printf 'FAILED: %s returned HTTP %s without the expected site HTML\n' "$url" "$status" >&2
    exit 1
  fi

  printf 'OK: %s returned HTTP %s and the expected site HTML\n' "$url" "$status"
done
