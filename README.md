# Blender NDOF Viewport Switcher

Exits fixed views when NDOF device motion exceeds threshold.

- For Blender 4.5 and 5.x
- Tested with 3DConnexion SpaceMouse Wireless

While you can always use the middle-mouse-btn to rotate out of an ortho (e.g. numpad 1 front view) or the camera view, it is not possible to do so with a SpaceMouse out-of-the-box.

With this Add-on however, you can force Blender to exit a fixed view into perspective view by pushing/rotating the NDOF device beyond a configurable threshold.

This video explains everything: https://youtu.be/xbDfJ20Jr8E


### Installation

- Download the ndof_viewport_switcher.py file
- In Blender open Preferences > Add-ons
- Use "Install from Disk" from the little dropdown in the top right corner of the Add-ons panel
- and install the ndof_viewport_switcher.py file

As long as the add-on is enabled, you can move/rotate out of a fixed view using your NDOF device (see video!)


### Add-on Preferences

You can set the Translation and Rotation thresholds in the Add-On's preferences. Higher values need stronger motion/force on the NDOF device to exit the fixed ortho/camera view.


### Contribute

Ideas that need YOU:
- Detect older Blender versions with different APIs to access the NDOF motion data and make this add-on work with Blender 4.4 and maybe even down to 3.6 (?)
- Turn this into an "extensions" for Blender 4+ instead of a legacy add-on
- Keep it working in the future with newer Blender/API versions
