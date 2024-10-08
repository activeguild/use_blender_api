import bpy
import re
import os
import subprocess

japanese_pattern = re.compile("[\u3040-\u30ff\u4e00-\u9faf]+")

japanese_objects = []
japanese_materials = []

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        if japanese_pattern.search(obj.name):
            japanese_objects.append(obj.name)

        if obj.data.materials:
            for mat in obj.data.materials:
                if mat and japanese_pattern.search(mat.name):
                    japanese_materials.append(mat.name)

output_file_path = bpy.path.abspath("//japanese_names_report.txt")

with open(output_file_path, 'w', encoding='utf-8') as f:
    if japanese_objects:
        f.write("日本語を含むオブジェクトの名前:\n")
        for name in japanese_objects:
            f.write(f" - {name}\n")
    else:
        f.write("日本語を含むオブジェクトは見つかりませんでした。\n")

    if japanese_materials:
        f.write("\n日本語を含むマテリアルの名前:\n")
        for name in japanese_materials:
            f.write(f" - {name}\n")
    else:
        f.write("日本語を含むマテリアルは見つかりませんでした。\n")

print(f"結果が {output_file_path} に出力されました。")

if os.name == 'nt':
    os.startfile(output_file_path)
elif os.name == 'posix': 
    subprocess.call(['open', output_file_path])