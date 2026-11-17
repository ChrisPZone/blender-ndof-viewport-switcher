# GNU General Public License v3.0 (see LICENSE)
# (C) 2025-2026 ChrisP


import bpy
from bpy.app.handlers import persistent
from math import fabs


# Utility to get the screen area under the mouse pointer
def view3d_area_under_mouse(context, event):
    x, y = event.mouse_x, event.mouse_y
    for area in context.window.screen.areas:
        if area.type == 'VIEW_3D' and area.x <= x < area.x + area.width and area.y <= y < area.y + area.height:
            return area
    return None


# Threshold Preferences
class NDOFViewportSwitcherPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    translation_threshold: bpy.props.FloatProperty(
        name="Translation Threshold",
        description="Minimum NDOF translation magnitude to trigger view switch",
        default=3,
        min=0.1,
        max=5.0,
        precision=1,
        step=10
    )
    rotation_threshold: bpy.props.FloatProperty(
        name="Rotation Threshold",
        description="Minimum NDOF rotation magnitude to trigger view switch",
        default=1,
        min=0.1,
        max=5.0,
        precision=1,
        step=10
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "translation_threshold")
        layout.prop(self, "rotation_threshold")


# Modal Operator to exit fixed ORTHO/CAMERA view when NDOF is moved beyond threshold in 3D-View
class NDOFViewportSwitchOperator(bpy.types.Operator):
    bl_idname = "view3d.ndof_viewport_switch"
    bl_label = "NDOF Viewport Switch"
    bl_options = {'INTERNAL'}

    # The one instance allowed to run; stale instances (e.g. after add-on re-enable) cancel themselves
    _active = None

    def modal(self, context, event):
        if self is not NDOFViewportSwitchOperator._active:
            return {'CANCELLED'}

        if event.type == 'NDOF_MOTION':
            addon = context.preferences.addons.get(__package__)
            if addon is None:
                # Add-on was disabled while this modal handler was still running
                return {'CANCELLED'}
            prefs = addon.preferences

            # Check threshold
            if (max(map(fabs, event.ndof_motion.translation)) > prefs.translation_threshold
                    or max(map(fabs, event.ndof_motion.rotation)) > prefs.rotation_threshold):
                area = view3d_area_under_mouse(context, event)
                if area:
                    region_3d = area.spaces.active.region_3d
                    perspective = region_3d.view_perspective

                    # Exit fixed view
                    if perspective in {'ORTHO', 'CAMERA'}:
                        region_3d.view_perspective = 'PERSP'
                        if perspective == 'CAMERA':
                            region_3d.view_distance = 10

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        NDOFViewportSwitchOperator._active = self
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "NDOF Viewport Switcher is ON")
        return {'RUNNING_MODAL'}


@persistent
def restart_operator(dummy):
    # Unregister any pending timer to avoid duplication, then schedule again
    if bpy.app.timers.is_registered(start_operator):
        bpy.app.timers.unregister(start_operator)
    bpy.app.timers.register(start_operator, first_interval=1)


def start_operator():
    if bpy.app.background:
        return None
    wm = bpy.context.window_manager
    if wm and wm.windows:
        with bpy.context.temp_override(window=wm.windows[0]):
            bpy.ops.view3d.ndof_viewport_switch('INVOKE_DEFAULT')
    return None


def register():
    bpy.utils.register_class(NDOFViewportSwitcherPreferences)
    bpy.utils.register_class(NDOFViewportSwitchOperator)
    bpy.app.handlers.load_post.append(restart_operator)
    # Start operator via timer to ensure safe context
    bpy.app.timers.register(start_operator, first_interval=1)


def unregister():
    if bpy.app.timers.is_registered(start_operator):
        bpy.app.timers.unregister(start_operator)
    bpy.app.handlers.load_post.remove(restart_operator)
    NDOFViewportSwitchOperator._active = None
    bpy.utils.unregister_class(NDOFViewportSwitchOperator)
    bpy.utils.unregister_class(NDOFViewportSwitcherPreferences)
