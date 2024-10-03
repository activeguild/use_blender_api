import bpy

def fix_inverted_normals():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"Fixed normals for {obj.name}")

fix_inverted_normals()