import os
import json

# ==== 路径配置 ====
json_path = r"E:\tmp for homework\ps-agent\data_cleaned.json"   # 原始 json
selected_data_dir = r"E:\tmp for homework\ps-agent\selected_data"  # 选中数据的根目录
output_json_path = r"E:\tmp for homework\ps-agent\data_selected.json"  # 输出的新 json

# ==== 读取 JSON ====
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==== 收集 selected_data 下所有图片文件名（不含路径）====
selected_files = set()
for root, _, files in os.walk(selected_data_dir):
    for file in files:
        name, ext = os.path.splitext(file)
        selected_files.add(name)   # 只存文件名（不带扩展名）

print(f"selected_data 下共找到 {len(selected_files)} 个文件名")

# ==== 筛选 JSON ====
new_data = {}
for key, item in data.items():
    # 判断条件：id 或 文件名在 selected_files 中
    origin_name = os.path.splitext(os.path.basename(item["origin_image_path"]))[0]
    ref_name = os.path.splitext(os.path.basename(item["reference_image_path"]))[0]

    if (key in selected_files):
        new_data[key] = item

print(f"从 {len(data)} 条数据筛选出 {len(new_data)} 条")

# ==== 保存新 JSON ====
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print(f"已保存筛选后的 JSON 文件：{output_json_path}")
