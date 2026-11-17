# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Blender extension (add-on, id `ndof_viewport_switcher`) that lets a 3D mouse (NDOF device, e.g. 3Dconnexion SpaceMouse) exit fixed views (ortho such as numpad front view, or camera view) into perspective when motion exceeds configurable thresholds. Targets Blender 4.2+ (README says tested on 4.5 and 5.x). Licensed GPL-3.0-or-later.

The entire add-on is `__init__.py`; metadata lives in `blender_manifest.toml`.

## Build & install

```bash
blender --command extension build
```

This produces `ndof_viewport_switcher-<version>.zip` (git-ignored). Install by drag-and-dropping the ZIP into Blender. Also available: `blender --command extension validate`.

There are no tests or linters; verification is manual in Blender with an NDOF device (or by checking the operator is running and inspecting `region_3d.view_perspective`).

## Architecture

- `NDOFViewportSwitchOperator` (`view3d.ndof_viewport_switch`) is a **permanently running modal operator** that always returns `{'PASS_THROUGH'}`, so it observes `NDOF_MOTION` events without consuming them — Blender's normal NDOF navigation still happens.
- On threshold breach it finds the `VIEW_3D` area **under the mouse pointer** (`view3d_area_under_mouse`), and if that view is `ORTHO` or `CAMERA` it sets `view_perspective = 'PERSP'`. Only when leaving `CAMERA` is `view_distance` reset to 10 (leaving ortho keeps the distance — intentional, see changelog v1.1).
- Startup: modal operators can't be invoked directly from `register()` (no valid window context), so `register()` schedules `startOperator` via `bpy.app.timers` (1 s delay).
- Modal handlers die when a new/different .blend file is loaded, so a `@persistent` `load_post` handler (`restartOperator`) re-schedules the timer. `unregister()` must remove that handler.
- Thresholds come from `NDOFViewportSwitcherPreferences`, read on every event via `context.preferences.addons[__package__]` — `__package__` is required (not a hardcoded name) because extensions are namespaced (`bl_ext.<repo>.ndof_viewport_switcher`).

## Conventions

- Blender extension rules apply (the code was cleaned up after extensions-team review): no legacy `bl_info` dict, metadata only in `blender_manifest.toml`.
- On release: bump `version` in `blender_manifest.toml` and add a dated entry to the Change Log in `README.md`.
- `README.md`, `.github/`, `.git/`, and ZIPs are excluded from the build via `[build].paths_exclude_pattern`; new non-runtime files should be added there too.
