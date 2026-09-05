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

    def modal(self, context, event):
        prefs = context.preferences.addons[__package__].preferences
        dt = prefs.translation_threshold
        dr = prefs.rotation_threshold

        if event.type == 'NDOF_MOTION':
            tx, ty, tz = event.ndof_motion.translation
            rx, ry, rz = event.ndof_motion.rotation

            # Check threshold
            if fabs(tx) > dt or fabs(ty) > dt or fabs(tz) > dt or fabs(rx) > dr or fabs(ry) > dr or fabs(rz) > dr:
                # area = next((a for a in context.screen.areas if a.type == 'VIEW_3D'), None)
                area = view3d_area_under_mouse(context, event)
                if area:
                    region_3d = area.spaces.active.region_3d
                    perspective = region_3d.view_perspective

                    # Exit fixed view
                    if perspective in {'ORTHO', 'CAMERA'}:
                        region_3d.view_perspective = 'PERSP'
                        if perspective == 'CAMERA':
                            region_3d.view_distance = 10
                        # return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "NDOF Viewport Switcher is ON")
        return {'RUNNING_MODAL'}


@persistent
def restartOperator(dummy):
    # Unregister any existing timer to avoid duplication
    try:
        bpy.app.timers.unregister(startOperator)
    except Exception:
        pass
    # Register timer/operator again
    bpy.app.timers.register(startOperator, first_interval=1)


def startOperator():
    if bpy.context.window_manager:
        bpy.ops.view3d.ndof_viewport_switch('INVOKE_DEFAULT')
    return None


def register():
    bpy.utils.register_class(NDOFViewportSwitcherPreferences)
    bpy.utils.register_class(NDOFViewportSwitchOperator)
    bpy.app.handlers.load_post.append(restartOperator)
    # Start operator via timer to ensure safe context
    bpy.app.timers.register(startOperator, first_interval=1)

def unregister():
    bpy.app.handlers.load_post.remove(restartOperator)
    bpy.utils.unregister_class(NDOFViewportSwitchOperator)
    bpy.utils.unregister_class(NDOFViewportSwitcherPreferences)

