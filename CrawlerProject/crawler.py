#数据来源：https://www.shanghairanking.cn/ 中国大学排名（主榜）
#Terminal --> pip install brotli 解压缩

import requests
from bs4 import BeautifulSoup
#导入所需的模块

def get_30_univs(year):
    #输入年份，返回对应年份的列表，元素为大学信息字典
    univs_data=[]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) RankingProject/147.0.0.0 Safari/537.36"
    }#请求头伪装

    url = f"https://www.shanghairanking.cn/rankings/bcur/{year}"#输入年份，得到相应url
    response = requests.get(url,headers=headers)#调用requests模块中get方法
    response.encoding = "utf-8"#utf-8支持中文编码
    soup = BeautifulSoup(response.text,"html.parser")#传输给BeautifulSoup解析html

    rows = soup.find_all("tr", attrs={"data-v-389300f0": True})

    #分析html
    for row in rows[1:]:
        # 排名
        rank = row.find("div", class_="ranking")
        rank = rank.text.strip() if rank else None
        rank = int(rank)

        # 中文名
        university = row.find("span", class_="name-cn")
        university = university.text.strip() if university else None

        # 标签（双一流/985/211）
        tag = row.find("p", class_="tags")
        tag = tag.text.strip() if tag else None

        # 所在地
        location_td = row.find_all("td")[2]  # 第三个 td
        location = location_td.text.strip() if location_td else None

        # 类型
        uni_type = row.find_all("td")[3]  # 第四个 td
        uni_type = uni_type.text.strip() if uni_type else None

        # 综合评分
        total_score = row.find_all("td")[4]  # 第五个 td
        total_score = total_score.text.strip() if total_score else None
        total_score = float(total_score)

        univs_data.append({
            "大学": university,
            "排名": rank,
            "类型": uni_type,
            "省市": location,
            "标签": tag,
            "总评分": total_score
        })

    return univs_data

#版本 148.0.7778.168（正式版本） （64 位）
#需下载对应版本 chrome 和 chromedrive，并放在当前path下
#下载地址https://sites.google.com/chromium.org/driver/downloads


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#导入所需模块

def get_500_univs(year):
    #输入年份，返回对应年份的列表，元素为大学信息字典

    driver = webdriver.Chrome()  # 初始化浏览器
    driver.get(f"https://www.shanghairanking.cn/rankings/bcur/{year}")# 输入年份，得到相应ur

    wait = WebDriverWait(driver, 5)
    univs_data = []

    while True:
        # 等待当前页的所有大学行加载完成
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[data-v-389300f0]")))
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-v-389300f0]")

        for row in rows:
            try:
                # 等待大学名可见
                name_elem = WebDriverWait(row, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.name-cn"))
                )
                university = name_elem.text.strip()

                # 排名
                rank_elem = row.find_element(By.CSS_SELECTOR, "div.ranking")
                rank = rank_elem.text.strip()
                if rank == "500+":
                   break
                   # 过滤掉500名后数据缺失的院校
                else:
                    rank = int(rank)
                    #将字符串转换为整数形式

                # 类型
                uni_type_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                uni_type = uni_type_elem.text.strip()

                # 省市
                location_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
                location = location_elem.text.strip()

                # 标签
                try:
                    tag_elem = row.find_element(By.CLASS_NAME, "tags")
                    tag = tag_elem.text.strip()
                except:
                    tag = None

                # 总评分
                total_score_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
                total_score = total_score_elem.text.strip()
                total_score = float(total_score)


                univs_data.append({
                    "大学": university,
                    "排名": rank,
                    "类型": uni_type,
                    "省市": location,
                    "标签":tag,
                    "总评分": total_score
                })
            except:
                # 如果某行数据抓取失败，跳过
                continue

        # 检查“下一页”按钮是否可点击
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next")
            if "disabled" in next_button.get_attribute("class"):
                break  # 已到最后一页，结束循环
            else:
                # 点击下一页
                link = next_button.find_element(By.CSS_SELECTOR, "a.ant-pagination-item-link")
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                link.click()
                time.sleep(2)  # 等待新一页加载
        except:
            break

    driver.quit()

    # 输出抓取结果
    return univs_data
