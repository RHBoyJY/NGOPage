import pandas as pd
import re

# 假設有一個 DataFrame 包含兩欄: "紀錄" 和 "Extracted_Key_Points"
data = {'紀錄': [" 1. 營養品需求評估 2. 體重78--->74kg 營養介入: 提供營養品維持化療期所需的熱量。",
               "2014.03.25 09:20 去電追蹤個案 PGSGA score: 2 points; PGSGA rating: stage A。 4. 營養診斷: (P)食物與營養相關知識不足"],
        'Extracted_Key_Points': [None, None]}

df = pd.DataFrame(data)

# 新增一欄名為 "記錄" 的欄位
df['記錄'] = [" 1. 營養品需求評估 2. 體重78--->74kg 營養介入: 提供營養品維持化療期所需的熱量。",
             "2014.03.25 09:20 去電追蹤個案 PGSGA score: 2 points; PGSGA rating: stage A。 4. 營養診斷: (P)食物與營養相關知識不足"]

# 關鍵點列表
extracted_key_points = [' PGSGA score', ' PGSGA rating', '營養診斷']

# 提取信息的函數
def extract_information(row):
    result_list = []
    for key_point in extracted_key_points:
        pattern = re.escape(key_point) + r'[\s\S]+?(?=\d+\.\s*|$)'
        extracted_info = re.search(pattern, row['記錄'])
        if extracted_info:
            result_list.append(extracted_info.group(0).strip())
        else:
            result_list.append(None)  # 如果没有匹配到，填入 None
    return pd.Series(result_list, index=extracted_key_points)

# 新增提取信息的列
df[extracted_key_points] = df.apply(extract_information, axis=1)

# 輸出結果
df