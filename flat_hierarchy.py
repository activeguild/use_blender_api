import bpy
import os

def load_glb(filepath):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    bpy.ops.import_scene.gltf(filepath=filepath)
    print(f"Loaded file: {filepath}")

def get_object_depth(obj):
    depth = 0
    while obj.parent is not None:
        depth += 1
        obj = obj.parent
    return depth

def fix_prim_encapsulation():
    fixes = []
    
    objects_to_process = sorted(bpy.data.objects, key=get_object_depth, reverse=True)
    for obj in objects_to_process:
        if obj.type in {'MESH', 'CURVE'}:
            parent = obj.parent
            if parent and parent.type in {'MESH', 'CURVE'}:
                world_location = obj.matrix_world.copy()

                obj.parent = None

                obj.matrix_world = world_location
                fixes.append(f"Moved {obj.name} to root from under {parent.name}")
    
    for material in bpy.data.materials:
        if "Shader" in material.name:
            if material.node_tree:
                connectable_nodes = [node for node in material.node_tree.nodes if node.type in {'GROUP', 'BSDF_PRINCIPLED', 'EMISSION'}]
                for node in connectable_nodes:
                    material.node_tree.nodes.remove(node)
                    fixes.append(f"Removed Connectable node {node.name} from Shader {material.name}")

    if fixes:
        print("The following changes were made:")
        for fix in fixes:
            print(fix)
    else:
        print("No encapsulation errors found. All rules are satisfied.")

def save_glb(output_filepath):
    bpy.ops.export_scene.gltf(filepath=output_filepath, export_format='GLB')
    print(f"File saved as: {output_filepath}")

input_filepath = "./test.glb"
output_filepath = "./output.glb"

if os.path.exists(input_filepath):
    load_glb(input_filepath)
    fix_prim_encapsulation()
    save_glb(output_filepath)
else:
    print(f"Input file not found: {input_filepath}")