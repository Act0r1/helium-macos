#!/usr/bin/env bash
set -euo pipefail

_root_dir="$(cd "$(dirname "$0")/.." && pwd)"
exec "$_root_dir/resources/compile_assets.sh"
