import os
import json
import sys

# ========== 配置区：根据实际路径修改 ==========
selected_data_dir = r"E:\tmp for homework\ps-agent\selected_data"
selected_data_0_dir = r"E:\tmp for homework\ps-agent\selected_data_0"
data_cleaned_json = r"E:\tmp for homework\ps-agent\data_cleaned.json"
# =============================================

def collect_filenames(root_dir):
    """
    遍历 root_dir，返回两个结构：
      - name2paths: dict, key=normed文件名(无扩展, 小写/规范化), value=list of full paths
      - names_set: set of normed 文件名
    """
    name2paths = {}
    for root, _, files in os.walk(root_dir):
        for fn in files:
            # 跳过隐藏文件或非图片（如果你想限制图片格式，可在这里判断扩展）
            if fn.startswith("."):
                continue
            name, ext = os.path.splitext(fn)
            # 规范化（Windows 下不区分大小写）
            norm_name = os.path.normcase(name.strip())
            full_path = os.path.join(root, fn)
            name2paths.setdefault(norm_name, []).append(full_path)
    return name2paths, set(name2paths.keys())

def load_data_cleaned_names(json_path):
    """
    读取 data_cleaned.json，收集 key，origin_image_path basename，reference_image_path basename
    返回集合（规范化后的小写/无扩展名）
    """
    names = set()
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[错误] 未找到 JSON 文件：{json_path}", file=sys.stderr)
        return names
    except Exception as e:
        print(f"[错误] 读取 JSON 出错：{e}", file=sys.stderr)
        return names

    for k, v in data.items():
        # key 本身也可能是我们需要比较的名字
        if k:
            names.add(os.path.normcase(str(k).strip()))
        # origin_image_path
        o = v.get("origin_image_path") if isinstance(v, dict) else None
        r = v.get("reference_image_path") if isinstance(v, dict) else None
        for path in (o, r):
            if path:
                base = os.path.splitext(os.path.basename(path))[0]
                names.add(os.path.normcase(base.strip()))
    return names

def main():
    print("正在扫描 selected_data ...")
    sel_map, sel_names = collect_filenames(selected_data_dir)
    print(f"selected_data 中文件（不含扩展名）数量 (unique names): {len(sel_names)}")

    print("正在扫描 selected_data_0 ...")
    sel0_map, sel0_names = collect_filenames(selected_data_0_dir)
    print(f"selected_data_0 中文件（不含扩展名）数量 (unique names): {len(sel0_names)}")

    print("正在读取 data_cleaned.json 中的文件名/key ...")
    cleaned_names = load_data_cleaned_names(data_cleaned_json)
    print(f"data_cleaned.json 中收集到的名字数量: {len(cleaned_names)}")

    # 查找：在 selected_data 中有、但 selected_data_0 中没有、且不在 data_cleaned.json 中的文件名
    to_report_paths = []  # 将打印这些文件的完整路径（可能有重复文件名对应多个路径）
    to_report_unique_names = set()

    for name, paths in sel_map.items():
        if (name not in sel0_names) and (name not in cleaned_names):
            # 这个名字满足条件，加入所有对应的文件路径
            to_report_paths.extend(paths)
            to_report_unique_names.add(name)

    # 打印结果
    if not to_report_paths:
        print("\n=== 结果 ===")
        print("未发现符合条件的图片（即：selected_data 有、selected_data_0 没有、且不在 data_cleaned.json 中的）。")
    else:
        print("\n=== 符合条件的图片列表（完整路径） ===")
        for p in to_report_paths:
            print(p)
        print("\n=== 汇总 ===")
        print(f"满足条件的文件总个数（含同名不同路径的每个文件）：{len(to_report_paths)}")
        print(f"满足条件的唯一文件名数量（不含扩展名）：{len(to_report_unique_names)}")

    # 可选：将结果写到文件，便于复查
    out_txt = os.path.join(os.path.dirname(data_cleaned_json), "selected_only_in_selected_data_report.txt")
    try:
        with open(out_txt, "w", encoding="utf-8") as f:
            if not to_report_paths:
                f.write("No files matched the criteria.\n")
            else:
                for p in to_report_paths:
                    f.write(p + "\n")
                f.write("\n")
                f.write(f"Total file paths: {len(to_report_paths)}\n")
                f.write(f"Unique base names: {len(to_report_unique_names)}\n")
        print(f"\n已将结果同时保存到：{out_txt}")
    except Exception as e:
        print(f"[警告] 无法写入报告文件：{e}", file=sys.stderr)


if __name__ == "__main__":
    main()
