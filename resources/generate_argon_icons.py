#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "helium-chromium/resources"))

from generate_branding import Transform, mark_svg


def main() -> None:
    assets = ROOT / "resources/assets"
    raw = Image.open(ROOT / "helium-chromium/resources/branding/app_icon/raw.png").convert("RGBA")
    face = raw.resize((824, 824), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (1024, 1024))
    alpha = Image.new("L", shadow.size)
    alpha.paste(face.getchannel("A"), (100, 112))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(12)).point(lambda value: round(value * 0.3)))
    shadow.alpha_composite(face, (100, 100))
    shadow.save(assets / "legacy.png")
    crop = raw.resize((512, 512), Image.Resampling.LANCZOS)
    crop.save(assets / "legacy_crop.png")
    shadow.save(assets / "app.icns", append_images=[crop.resize((size, size), Image.Resampling.LANCZOS) for size in (16, 32, 64)])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">'
        + mark_svg(Transform(3.21875, 512, 512), "#FFFFFF", "#FFFFFF")
        + "</svg>\n"
    )
    (assets / "AppIcon.icon/Assets/logo.svg").write_text(svg)
    icon_path = assets / "AppIcon.icon/icon.json"
    icon = json.loads(icon_path.read_text())
    icon["fill-specializations"][0]["value"]["linear-gradient"] = [
        "srgb:0.14902,0.14902,0.16471,1.00000",
        "srgb:0.05490,0.05490,0.06275,1.00000",
    ]
    layer = icon["groups"][0]["layers"][0]
    layer["position"]["scale"] = 1
    for fill in layer["fill-specializations"]:
        fill["value"]["solid"] = "srgb:1.00000,1.00000,1.00000,1.00000"
    icon_path.write_text(json.dumps(icon, indent=2, separators=(",", " : ")) + "\n")


if __name__ == "__main__":
    main()
