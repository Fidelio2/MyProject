from collections import Counter
import matplotlib.pyplot as plt
# 关键的数据可视化库


def setup_chinese_font():
    # 指定 Matplotlib 绘图使用中文字体，防止乱码
    plt.rcParams["font.sans-serif"] = [
        "PingFang SC",
        "Hiragino Sans GB",
        "Heiti SC",
        "Arial Unicode MS",
        "SimHei",
    ]
    plt.rcParams["axes.unicode_minus"] = False




def plot_score_bar(data, path, year):
    # 横向柱状图 – 总评分
    names = [item["大学"] for item in data]
    scores = [item["总评分"] for item in data]

    plt.figure(figsize=(12, 9))
    plt.barh(names[::-1], scores[::-1], color="#2F80ED")
    plt.title(f"{year} 软科中国大学排名 Top {len(data)} 总评分")
    plt.xlabel("总评分")
    plt.ylabel("大学")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_score_line(data, path, year):
    # 折线图 – 排名 总评分
    ranks = [item["排名"] for item in data]
    scores = [item["总评分"] for item in data]

    plt.figure(figsize=(10, 6))
    plt.plot(ranks, scores, marker="o", linewidth=2.2, color="#27AE60")
    plt.title(f"{year} Top {len(data)} 排名与总评分折线图")
    plt.xlabel("排名")
    plt.ylabel("总评分")
    plt.grid(alpha=0.25) #添加网格，提高可读性
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_location_distribution(data, path, year):
    # 柱状图 – 高校省市分布
    location_counts = Counter(item["省市"] for item in data if item["省市"])
    labels, values = zip(*location_counts.most_common())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="#F2994A")
    plt.title(f"{year} Top {len(data)} 高校省市分布")
    plt.xlabel("省市")
    plt.ylabel("高校数量")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_type_distribution(data, path, year):
    # 饼图 – 高校类型占比
    type_counts = Counter(item["类型"] for item in data if item["类型"])
    labels, values = zip(*type_counts.most_common())

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"{year} Top {len(data)} 高校类型占比")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
