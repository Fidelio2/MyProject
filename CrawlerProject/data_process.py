import csv
import json
from pathlib import Path



def load_data(data,limit=30):
    # 获取data，保留前N项,N默认为30
    return data[:limit]

def save_json(data, path):
    # 将数据保存为 JSON
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, path):
    # 将数据保存为 CSV
    if not data:
        return

    fieldnames = ["排名", "大学", "类型", "省市", "标签", "总评分"]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def save_data_files(data, output_dir):
    #保存 JSON 和 CSV 到指定目录
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / "university_ranking.json"
    csv_path = output_dir / "university_ranking.csv"

    save_json(data, json_path)
    save_csv(data, csv_path)
