import os
import json

# ==== 路径配置 ====
json_path = r"E:\tmp for homework\ps-agent\distill_data.json"   # 你的原始json文件路径
images_dir = r"E:\tmp for homework\ps-agent\images"    # 图片目录
output_json_path = r"E:\tmp for homework\ps-agent\data_cleaned.json"  # 输出的新json

# ==== 第一步：读取 json 并保留指定字段 ====
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 新字典
new_data = {}
valid_images = set()  # 用于记录合法的图片路径

for key, item in data.items():
    filtered_item = {
        "id": item.get("id"),
        "origin_image_path": item.get("origin_image_path"),
        "reference_image_path": item.get("reference_image_path"),
        "instruction": item.get("instruction")
    }
    new_data[key] = filtered_item
    
    # 记录保留的图片路径（转成小写+绝对路径防止大小写不一致）
    if filtered_item["origin_image_path"]:
        valid_images.add(os.path.normcase(filtered_item["origin_image_path"]))
    if filtered_item["reference_image_path"]:
        valid_images.add(os.path.normcase(filtered_item["reference_image_path"]))

# 保存新的 json
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print(f"已生成精简后的 JSON 文件：{output_json_path}")

# ==== 第二步：删除未在 JSON 出现过的图片 ====
deleted_files = []
for file in os.listdir(images_dir):
    file_path = os.path.join(images_dir, file)
    norm_path = os.path.normcase(file_path)
    if norm_path not in valid_images:
        os.remove(file_path)
        deleted_files.append(file_path)

print(f"已删除 {len(deleted_files)} 个未使用的图片")
