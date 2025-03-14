import bpy

input_path = "./input.glb"  
output_path = "./output.glb"

def fix_inverted_normals():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"Fixed normals for {obj.name}")

def process_glb(input_path, output_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=input_path)

    # 法線を修正
    fix_inverted_normals()
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"Exported fixed GLB to {output_path}")

process_glb(input_path, output_path)
