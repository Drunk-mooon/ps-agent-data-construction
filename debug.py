import json

def add_prompt_to_instructions(json_file_path):
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 修改每个instruction
    for key in data:
        if 'instruction' in data[key]:
            data[key]['instruction'] = f"```[prompt]```{data[key]['instruction']}"
    
    # 写回JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f"已成功修改 {len(data)} 个instruction")

# 使用示例
json_file_path = 'data_selected.json'  # 替换为你的JSON文件路径
add_prompt_to_instructions(json_file_path)