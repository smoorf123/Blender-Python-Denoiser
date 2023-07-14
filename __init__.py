bl_info = {
    "name": "Denoiser Select Add-on",
    "author": "Somil Varshney",
    "warning": "Python libraries are automatically installed using the internet.",
    "description": "Add-on that allows users to denoise using custom denoising algorithms",
    "version": (0, 1),
    "blender": (2, 80, 0)
}

import os
import sys
import subprocess

try:
    ## INSTALL REQUIRED MODULES
    # path to python.exe
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

    # upgrade pip
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# install required packages
    for package in ["bm3d", "scipy", "numpy", "opencv-python", "scikit-image"]:
        subprocess.call([python_exe, "-m", "pip", "install", package])

    print("Required Modules Installed")
except:
    raise Exception("Required Modules could not be installed, please check your internet connection and re-register the addon (Edit > Preferences > Add-ons > Denoiser Select)")


from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator
from bpy.props import PointerProperty
import bpy

from .Advanced_Denoisers import *
from .Traditional_Denoisers import *
from .denoiser_functions import denoise, denoise_preview


FILE_PATH = ""
render_num = 1
function_selected = ""

functions_dict = {"Gaussian": gaussian_denoising.gaussian_dn, "Mean": mean_denoising.mean_dn, 
                  "Median": median_denoising.median_dn, "Bilateral": bilateral_denoising.bilateral_dn, 
                  "BM3D": bm3d_denoising.bm3d_dn, "NLM": non_local_means_denoising.nlm_dn, 
                  "TV": total_variation_denoising.tv_dn, "Wavelet": wavelet_denoising.wavelet_dn}

def render():

    # Render Settings
    print("Rendering...")

    bpy.context.scene.render.filepath = f"{FILE_PATH}\\non_denoised_{render_num}"
    bpy.ops.render.render(write_still=True)

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
        global FILE_PATH

        FILE_PATH = os.path.join(os.path.split(self.filepath)[
                                 0])

        print("Files will be saved here: ", FILE_PATH)
        return {'FINISHED'}

class DENOISER_PREVIEW_operator(Operator):
    '''See a preview of the denoised output using the chosen algorithm'''
    bl_idname = "dn_prv.operator"
    bl_label = "Denoise Preview"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        function_selected = bpy.context.scene.scene_propname.my_enum

        if FILE_PATH:
            render()
            denoise_preview(f"{FILE_PATH}\\non_denoised_{render_num}.png", functions_dict[function_selected])  # run denoiser and preview
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
        global render_num
        function_selected = bpy.context.scene.scene_propname.my_enum

        if FILE_PATH:
            render()
            denoise(f"{FILE_PATH}\\non_denoised_{render_num}.png", f"{FILE_PATH}\\{function_selected}_denoised_{render_num}.png", functions_dict[function_selected])  # run denoiser
            render_num+=1
            self.report(
                {"INFO"}, "The Denoised render has been saved to the chosen location.")
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

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_propname

if __name__ == '__main__':
    register()