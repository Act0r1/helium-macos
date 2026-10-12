#!/usr/bin/env bash
set -euo pipefail

_root_dir="$(cd "$(dirname "$0")/.." && pwd)"
_assets="$_root_dir/resources/assets"
_compiler="$_root_dir/build/src/tools/mac/icons/compile_car.py"

if [ "$(uname -s)" != Darwin ]; then
  echo "Assets.car requires macOS and Xcode 26." >&2
  exit 1
fi
if [ ! -f "$_compiler" ]; then
  echo "Prepare Chromium sources in build/src before compiling Assets.car." >&2
  exit 1
fi

mkdir -p "$_root_dir/resources/generated"
_stage="$(mktemp -d "$_root_dir/resources/generated/argon-assets.XXXXXX")"
trap 'rm -rf "$_stage"' EXIT
cp -R "$_assets/Assets.xcassets" "$_assets/AppIcon.icon" "$_stage/"

python3 - "$_assets" "$_stage" <<'PY'
import sys
from pathlib import Path
from PIL import Image

assets, stage = map(Path, sys.argv[1:])
for size in (16, 32, 64, 128, 256, 512):
    source = assets / ("legacy_crop.png" if size <= 32 else "legacy.png")
    with Image.open(source) as image:
        image.resize((size, size), Image.Resampling.LANCZOS).save(
            stage / "Assets.xcassets/AppIcon.appiconset" / f"appicon_{size}.png"
        )
PY

python3 "$_compiler" --verbose "$_stage/Assets.xcassets"
cp "$_stage/Assets.car" "$_assets/Assets.car"
