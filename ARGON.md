# Argon for macOS

Argon adds workspaces and password saving to Helium. This fork uses core commit
`d9004cc076000d5a08bc11417edcfe93ac36ed4b` from `Act0r1/helium`, branch `ws`.

```sh
git clone --recursive https://github.com/Act0r1/helium-macos.git
cd helium-macos
```

Use macOS 12+, Xcode 26 with its Metal toolchain, and the Homebrew/Python
dependencies in [docs/building.md](docs/building.md). Open Xcode once, then run:

```sh
./build.sh -d arm64
# On Intel, or for an Intel build:
./build.sh -d x86_64
```

The output is `build/argon_<version>-<revision>.<platform>_macos.dmg`, containing
`Argon.app`. Without `MACOS_CERTIFICATE_NAME`, packaging uses ad-hoc signing.
Developer ID signing and notarization use the existing optional environment
variables documented in the build guide.

## Icons and packaging

The committed PNG/ICNS files and Icon Composer SVG come from the core Argon
assets and geometry. Regenerate them with Python and Pillow:

```sh
python3 resources/generate_argon_icons.py
```

`resources/assets/Assets.car` is still the upstream Helium binary: Linux cannot
compile Apple's asset catalogs. On macOS, resource preparation automatically
runs `resources/compile_assets.sh` after downloading Chromium sources. It uses
Chromium's `tools/mac/icons/compile_car.py` and Xcode `actool` to rebuild the
catalog from `AppIcon.icon`, retaining the committed fallback `app.icns`.
To regenerate the catalog manually once `build/src` is prepared:

```sh
./resources/compile_assets.sh
```

Commit the regenerated `resources/assets/Assets.car` on a Mac. Verify the icon
in Finder/Dock on both older macOS and macOS 26 before release.
The DMG layout now names `Argon.app`; its Mac regeneration command is
`./devutils/generate_dmg_dsstore.sh` (requires Node/npm for `appdmg`).

## Compatibility and verification

Bundle ID `net.imput.helium`, profile directories, `helium://`, and keychain
service/account names remain unchanged. `Helium.provisionprofile` is an internal
signing input, also unchanged. Argon and Helium share these existing identities.

Core disables browser updates: Sparkle startup, manual checks, and its delegate
use `ShouldAccessUpdateService`; `GetBrowserUpdateURL` returns core's dummy URL.
Component updates and other Helium services are separate and retain core behavior.

Linux verification covered all eight files shared by the workspace patches and
macOS patches, applying core first with zero fuzz. Relevant hunks applied across
95 files. Three external Sparkle source files were unavailable in the Linux
reference tree and need verification after macOS dependencies are downloaded.
A full macOS build, signing/notarization, DMG installation, keychain continuity,
workspace/fullscreen behavior, and runtime updater network checks remain to be
verified on a Mac. The upstream manual submodule-bump workflow tracks `main`;
do not use it to update this fork's pinned `ws` core.
