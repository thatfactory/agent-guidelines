#!/usr/bin/env bash

set -euo pipefail

usage() {
    echo "Usage: $0 <format|lint|lint-strict> <path>..." >&2
}

if [[ $# -lt 2 ]]; then
    usage
    exit 64
fi

mode="$1"
shift

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
configuration="$script_directory/../Configurations/Swift/.swift-format"

if command -v xcrun >/dev/null 2>&1 && xcrun --find swift-format >/dev/null 2>&1; then
    formatter=(xcrun swift-format)
elif command -v swift-format >/dev/null 2>&1; then
    formatter=(swift-format)
elif command -v swift >/dev/null 2>&1; then
    formatter=(swift format)
else
    echo "error: swift-format is unavailable; install or select a Swift 6 toolchain." >&2
    exit 127
fi

common_arguments=(
    --configuration "$configuration"
    --recursive
    --parallel
)

case "$mode" in
    format)
        "${formatter[@]}" format --in-place "${common_arguments[@]}" "$@"
        ;;
    lint)
        "${formatter[@]}" lint "${common_arguments[@]}" "$@"
        ;;
    lint-strict)
        "${formatter[@]}" lint --strict "${common_arguments[@]}" "$@"
        ;;
    *)
        usage
        exit 64
        ;;
esac
