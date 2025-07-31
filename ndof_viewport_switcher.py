# GNU General Public License v3.0 (see LICENSE)
# (C) 2025 ChrisP


bl_info = {
    "name": "NDOF Viewport Switcher",
    "author": "ChrisP",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "View3D",
    "description": "Exits fixed views when NDOF device motion exceeds threshold",
    "category": "3D View",
}


import bpy
from math import fabs


# Threshold Preferences
class NDOFViewportSwitcherPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    translation_threshold: bpy.props.FloatProperty(
        name="Translation Threshold",
        description="NDOF movement sensitivity",
        default=3,
        min=0.1,
        max=5.0,
        precision=1,
        step=0.1
    )
    rotation_threshold: bpy.props.FloatProperty(
        name="Rotation Threshold",
        description="NDOF movement sensitivity",
        default=1,
        min=0.1,
        max=5.0,
        precision=1,
        step=0.1
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
        prefs = context.preferences.addons[__name__].preferences
        dt = prefs.translation_threshold
        dr = prefs.rotation_threshold

        if event.type == 'NDOF_MOTION':
            tx, ty, tz = event.ndof_motion.translation
            rx, ry, rz = event.ndof_motion.rotation

            # Check threshold
            if fabs(tx) > dt or fabs(ty) > dt or fabs(tz) > dt or fabs(rx) > dr or fabs(ry) > dr or fabs(rz) > dr:
                area = next((a for a in context.screen.areas if a.type == 'VIEW_3D'), None)
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
        return {'RUNNING_MODAL'}


def startOperator():
    if bpy.context.window_manager:
        bpy.ops.view3d.ndof_viewport_switch('INVOKE_DEFAULT')
    return None


def register():
    bpy.utils.register_class(NDOFViewportSwitcherPreferences)
    bpy.utils.register_class(NDOFViewportSwitchOperator)
    # Start operator via timer to ensure safe context
    bpy.app.timers.register(startOperator, first_interval=1)

def unregister():
    bpy.utils.unregister_class(NDOFViewportSwitchOperator)
    bpy.utils.unregister_class(NDOFViewportSwitcherPreferences)

if __name__ == "__main__":
    register()
