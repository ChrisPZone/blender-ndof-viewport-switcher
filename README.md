# Blender NDOF Viewport Switcher

Exits fixed views when NDOF device motion exceeds threshold.

- For Blender 4.5 and 5.x
- Tested with 3DConnexion SpaceMouse Wireless

While you can always use the middle-mouse-btn to rotate out of an ortho (e.g. numpad 1 front view) or the camera view, it is not possible to do so with a SpaceMouse out-of-the-box.

With this Add-on however, you can force Blender to exit a fixed view into perspective view by pushing/rotating the NDOF device beyond a configurable threshold.

This video explains things: https://youtu.be/xbDfJ20Jr8E
(Note: The video was recorded for version 1, the add-on has improved since)


## Installation

- In Blender open "Preferences" > "Get Extenstions"
- Search for "NDOF Viewport Switcher"
- Click "Install"

As long as the add-on is **enabled**, you can move/rotate out of a fixed view using your NDOF device (see video!)


## Add-on Preferences

You can set the Translation and Rotation thresholds in the Add-On's preferences. Higher values need stronger motion/force on the NDOF device to exit the fixed ortho/camera view.


## Local Build & Install

- Build: ```blender --command extension build```
- Install: Drag-And-Drop the generated ZIP file into Blender


## Change Log

- v1.3.1 @ 2026-09-03
  - Add-On is now a Blender Extension
- v1.3 @ 2026-04-13
  - Only affect the 3D view under the mouse pointer
- v1.2 @ 2025-09-04
  - Restart operator when opening a different/new file
- v1.1 @ 2025-07-31
  - Don't reset view distance when coming from ORTHO view

