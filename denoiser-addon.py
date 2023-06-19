bl_info = {
    "name": "Denoiser Select Add-on",
    "author": "Somil",
    "version": (0, 1),
    "blender": (2, 80, 0)
}

import bpy

render = bpy.context.scene.render
scale = render.resolution_percentage / 100

WIDTH = int(render.resolution_x * scale)
HEIGHT = int(render.resolution_y * scale)

FILE_NAME = "nondenoised.png"
FILE_PATH = fr"/{FILE_NAME}"

FILE_PATH_MODIFIED = r"denoised.png"

def render_and_denoise():
    render()
    
def render():
    print("Rendering...")
    
    previous_path = bpy.context.scene.render.filepath
    bpy.context.scene.render.filepath = FILE_PATH

    bpy.ops.render.render(write_still=True)

    bpy.context.scene.render.filepath = previous_path
    
    print("Rendering complete.")
    
render_and_denoise()





