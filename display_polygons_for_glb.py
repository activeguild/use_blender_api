import bpy
import os

def load_glb(filepath):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=filepath)

def get_mesh_polygon_counts():
    mesh_polygon_counts = []
    total_polygon_count = 0 
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            polygon_count = len(obj.data.polygons)
            mesh_polygon_counts.append((obj.name, polygon_count))
            total_polygon_count += polygon_count
    
    mesh_polygon_counts.sort(key=lambda x: x[1], reverse=True)
    
    return mesh_polygon_counts, total_polygon_count

def process_glb_file(filepath):
    load_glb(filepath)
    
    mesh_polygon_counts, total_polygon_count = get_mesh_polygon_counts()
    
    print(f"GLBファイル: {os.path.basename(filepath)}")
    for mesh_name, polygon_count in mesh_polygon_counts:
        print(f"メッシュ名: {mesh_name}, ポリゴン数: {polygon_count}")
    
    print(f"合計ポリゴン数: {total_polygon_count}")

def batch_process_glb_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".glb"):
            filepath = os.path.join(directory, filename)
            process_glb_file(filepath)

if __name__ == "__main__":
    directory_path = "./glb"
    
    batch_process_glb_directory(directory_path)