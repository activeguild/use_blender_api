import bpy

# GLBの入出力パスを指定
input_glb_path = "./input.glb"  # 読み込むGLBファイル
output_glb_path = "./output.glb"

# 既存のオブジェクトを削除
bpy.ops.wm.read_factory_settings(use_empty=True)

# GLBファイルをインポート
bpy.ops.import_scene.gltf(filepath=input_glb_path)

# シーン内のオブジェクトを取得
objects = bpy.context.scene.objects

# 親オブジェクトを特定（子オブジェクトの親がMESHの場合）
parent = None
for obj in objects:
    if obj.parent and obj.parent.type == 'MESH':
        parent = obj.parent
        break  # 最初に見つかった親を使用

if not parent:
    print("親メッシュが見つかりません。スクリプトを終了します。")
else:
    print(f"親メッシュ: {parent.name}")  # 親メッシュの名前を出力

    # 親の子オブジェクトを取得（メッシュのみ）
    children = [obj for obj in objects if obj.parent == parent and obj.type == 'MESH']

    if not children:
        print("子メッシュが見つかりません。スクリプトを終了します。")
    else:
        print("子メッシュ: ", [child.name for child in children])  # 子メッシュの名前をリスト表示

        # 親のアニメーションデータをバックアップ
        if parent.animation_data and parent.animation_data.action:
            backup_action = parent.animation_data.action.copy()
        else:
            backup_action = None

        # JOIN前の親のトランスフォームを保存
        original_parent_matrix = parent.matrix_world.copy()

        # 親のアニメーションをワールド座標に適用
        bpy.ops.object.select_all(action='DESELECT')
        parent.select_set(True)
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.visual_transform_apply()

        # 子メッシュを親のワールド座標に合わせて移動
        for child in children:
            child.select_set(True)
            child.matrix_world = parent.matrix_world @ child.matrix_local
        
        # JOIN実行
        bpy.ops.object.join()

        # JOIN後、親の位置を復元
        parent.matrix_world = original_parent_matrix

        # JOIN後、アニメーションデータを元に戻す
        if backup_action:
            parent.animation_data.action = backup_action
            # Fカーブの座標修正（ローカル座標系のズレを防ぐ）
            for fcurve in backup_action.fcurves:
                if "location" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.co.y += original_parent_matrix.to_translation().y

        # GLBエクスポート設定
        export_settings = {
            "filepath": output_glb_path,
            "export_format": 'GLB',
            "export_apply": True,
            "export_animations": True,
        }

        # エクスポート
        bpy.ops.export_scene.gltf(**export_settings)

        print(f"GLBエクスポート完了: {output_glb_path}")
