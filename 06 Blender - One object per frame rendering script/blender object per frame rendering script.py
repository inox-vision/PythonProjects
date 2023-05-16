# renders each object in a separate frame
# names image files after original 3D objects 
# places those renders in directories
# named after collections

import bpy

all_objects = bpy.data.objects
bpy.ops.object.select_all(action='SELECT')
cur_frame=0
filepath = "//../RENDER/"

for collection in bpy.data.collections:
    for obj in collection.objects:
        bpy.context.scene.frame_set(cur_frame)
        for all_obj in all_objects:
            all_obj.hide_render = 1 # Hidng all objects in render   
        
        obj.hide_render = 0    # Unhiding only one object
        bpy.context.scene.render.filepath = filepath + str("/") + collection.name + str("/") + obj.name
        bpy.ops.render.render(write_still=True)
        cur_frame += 1


