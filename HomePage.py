import time

import streamlit as st

import numpy as np
import pandas as pd
import re
from io import StringIO, BytesIO

def find_header_location(df):
    # 尋找標題所在的位置，這裡簡單示範在每行每列中找到第一個不為空的單元格作為標題位置
    for index, row in df.iterrows():
        for col_index, value in enumerate(row):
            if pd.notna(value):
                return index, col_index
    return None, None

def process_excel_data(byte_data):
    # 將二進制數據轉換為BytesIO對象
    excel_data = BytesIO(byte_data)

    # 讀取 Excel 檔案
    df = pd.read_excel(excel_data, engine='openpyxl')

    # 分析最後一欄的資料
    last_column_name = df.columns[-1]
    df['New_Column'] = df[last_column_name].apply(lambda x: extract_bullet_points(x))

    # 假設 your_custom_function 是你用來處理最後一欄資料的自訂函數
    # 你可以在這裡自行定義 your_custom_function

    # 將處理後的數據轉換為新的 Excel 檔案
    output_excel = BytesIO()
    df.to_excel(output_excel, index=False, engine='openpyxl')

    # 取得最終的二進制數據
    output_excel_data = output_excel.getvalue()

    return output_excel_data


def extract_bullet_points(text):
    # 利用正則表達式找到以"A："為開頭的句子，並將其分割成要點
    points = re.split(r'目的：', text)[1:]

    # 清理要點中的空格和換行符號
    points = [point.strip() for point in points]

    return points

st.title('我的第一個應用程式')

st.write("嘗試創建**checkbox**：")
if st.checkbox('資料比對'):
    uploaded_file1 = st.file_uploader("請上傳Excel檔案一")
    if uploaded_file1 is not None:
        # To read file as bytes:
        bytes_data = uploaded_file1.getvalue()
        result_byte_data = process_excel_data(bytes_data)
        st.download_button(
            label="Download data as Excel",
            data=result_byte_data,
            file_name='large_df.xlsx',
            mime='Excel/xlsx',
        )

    uploaded_file2 = st.file_uploader("請上傳Excel檔案二")
    if uploaded_file2 is not None:
        # To read file as bytes:
        bytes_data = uploaded_file2.getvalue()
        result_byte_data = process_excel_data(bytes_data)
        st.download_button(
            label="Download data as Excel",
            data=result_byte_data,
            file_name='large_df.xlsx',
            mime='Excel/xlsx',
        )

if st.checkbox('資料關鍵資訊整理'):
    uploaded_file = st.file_uploader("請上傳Excel檔案一")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        result_byte_data = process_excel_data(bytes_data)
        st.download_button(
            label="Download data as Excel",
            data=result_byte_data,
            file_name='large_df.xlsx',
            mime='Excel/xlsx',
        )

st.write("嘗試創建**Button**：")
if st.button('按一下!'):
    # st.text("乖!真乖!!!")
    st.balloons()
if st.button('按一下下雪!'):
    st.snow()

st.write("嘗試創建**表格**：")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
df

st.write("嘗試創建**Chart**：")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

st.write("嘗試創建**MAP**：")
if st.checkbox('顯示地圖圖表'):
    map_data = pd.DataFrame(
        np.random.randn(50, 2) / [2, 2] + [23.58, 120.58],
        columns=['lat', 'lon'])
    st.map(map_data)

st.write("嘗試創建**下拉選單**：")
option = st.sidebar.selectbox(
    '你喜歡哪種動物？',
    ['狗', '貓', '鸚鵡', '天竺鼠'])
st.text(f'你的答案：{option}')
# st.sidebar.text(f'你的答案：{option}')

st.write("嘗試創建**左右欄位**：")
left_column, right_column = st.columns(2)
left_column.write("這是左邊欄位。")
right_column.write("這是右邊欄位。")

st.write("嘗試創建**隱藏選項**：")
expander = st.expander("點擊來展開...")
expander.write(" 方案1。")
expander.write(" 方案2。")


