bl_info = {
    "name": "Denoiser Select Add-on",
    "author": "Somil",
    "version": (0, 1),
    "blender": (2, 80, 0)
}

from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator
from bpy.props import PointerProperty
import bpy

import os
from denoiser_functions import denoise, denoise_preview
from Advanced_Denoisers import *
from Traditional_Denoisers import *

FILE_PATH = ""
FILE_PATH_DENOISED = ""
function_selected = ""

functions_dict = {"Gaussian": gaussian_denoising.gaussian_dn, "Mean": mean_denoising.mean_dn, 
                  "Median": mean_denoising.median_dn, "Bilateral": bilateral_denoising.bilateral_dn, 
                  "BM3D": bm3d_denoising.bm3d_dn, "NLM": non_local_means_denoising.nlm_dn, 
                  "TV": total_variation_denoising.tv_dn, "Wavelet": wavelet_denoising.wavelet_dn}

def render():

    # Render Settings
    render = bpy.context.scene.render
    scale = render.resolution_percentage / 100

    WIDTH = int(render.resolution_x * scale)
    HEIGHT = int(render.resolution_y * scale)

    print("Rendering...")

    previous_path = bpy.context.scene.render.filepath
    bpy.context.scene.render.filepath = FILE_PATH

    bpy.ops.render.render(write_still=True)

    bpy.context.scene.render.filepath = previous_path

    print("Rendering complete.")

class CustomDenoiser(bpy.types.PropertyGroup):

    my_enum : bpy.props.EnumProperty(name="", description="Choose Denoising Algorithm",
                                    items=(
                                        ('Gaussian', "Gaussian",
                                         "Gaussian Denoising, Traditional Denoiser"),
                                        ('Mean', "Mean",
                                         "Mean Denoising, Traditional Denoiser"),
                                        ('Median', "Median",
                                         "Median Denoising, Traditional Denoiser"),
                                        ('Bilateral', "Bilateral",
                                         "Bilateral Denoising, Advanced Denoiser"),
                                        ('BM3D', "BM3D",
                                         "BM3D Denoising, Advanced Denoiser"),
                                        ('NLM', "NLM",
                                         "Non-Local Means Denoising, Advanced Denoiser"),
                                        ('TV', "Total Variation",
                                         "Total Variation Denoising, Advanced Denoiser"),
                                        ('Wavelet', "Wavelet",
                                         "Wavelet Denoising, Advanced Denoiser")
                                    ))
    
class SetSavePath(Operator, ImportHelper):
    '''Set the destination of both the noisy and denoised versions of the render'''
    bl_idname = "set_path.operator"
    bl_label = "Set Save Location"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        global FILE_PATH, FILE_PATH_DENOISED

        FILE_PATH = os.path.join(os.path.split(self.filepath)[
                                 0], "non-denoised.png").replace("\\", "/")
        FILE_PATH_DENOISED = os.path.join(
            FILE_PATH, "denoised.png").replace("\\", "/")

        return {'FINISHED'}


class DENOISER_PREVIEW_operator(Operator):
    '''See a preview of the denoised output using the chosen algorithm'''
    bl_idname = "dn_prv.operator"
    bl_label = "Denoise Preview"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        if FILE_PATH:
            render()
            denoise_preview(FILE_PATH, functions_dict[function_selected])  # run denoiser and preview
        else:
            self.report(
                {"ERROR"}, "You may not have set the save destination!")

        return {'FINISHED'}


class DENOISE_operator(Operator):
    '''Render, Denoise and Save the Output to a Chosen Location'''
    bl_idname = "dn.operator"
    bl_label = "Denoise"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        if FILE_PATH:
            render()
            denoise(FILE_PATH, FILE_PATH_DENOISED, functions_dict[function_selected])  # run denoiser
        else:
            self.report(
                {"ERROR"}, "You may not have set the save destination!")

        return {'FINISHED'}


class DENOISER_PT_rendersettings(Panel):
    """ Tooltip """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Custom Denoiser"
    bl_category = "Custom Denoiser"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("set_path.operator", icon="NONE")

        layout.label(text="Choose an Algorithm:")
        prop_one = scene.scene_propname
        layout.prop(prop_one, "my_enum")
        box = layout.box()

        row = box.row()
        row.scale_y = 1.5
        row.operator("dn_prv.operator", icon="NONE")

        row = box.row()
        row.scale_y = 1.5
        row.operator("dn.operator", icon="NONE")


classes = [
    CustomDenoiser,
    SetSavePath,
    DENOISER_PREVIEW_operator,
    DENOISE_operator,
    DENOISER_PT_rendersettings
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.scene_propname = PointerProperty(type=CustomDenoiser)
    function_selected = bpy.context.scene.scene_propname.my_enum

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_propname


if __name__ == '__main__':
    register()