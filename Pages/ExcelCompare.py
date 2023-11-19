import time

import streamlit as st

import numpy as np
import pandas as pd
from io import BytesIO

def find_header_location(df):
    # 尋找標題所在的位置，這裡簡單示範在每行每列中找到第一個不為空的單元格作為標題位置
    for index, row in df.iterrows():
        for col_index, value in enumerate(row):
            if pd.notna(value):
                return index, col_index
    return None, None

def combine_titles(df1, df2, header_row1, header_col1, header_row2, header_col2):
    # 獲取第一個檔案的標題
    title1 = df1.iloc[header_row1, header_col1]

    # 獲取第二個檔案的標題
    title2 = df2.iloc[header_row2, header_col2]

    # 組合兩個檔案的標題
    combined_title = f"{title1}_{title2}"

    return combined_title

def process_excel_data(byte_data1, byte_data2):
    # 讀取第一個 Excel 檔案
    df1 = pd.read_excel(BytesIO(byte_data1), engine='openpyxl')

    # 找出第一個檔案的標題位置
    header_row1, header_col1 = find_header_location(df1)

    # 讀取第二個 Excel 檔案
    df2 = pd.read_excel(BytesIO(byte_data2), engine='openpyxl')

    # 找出第二個檔案的標題位置
    header_row2, header_col2 = find_header_location(df2)

    # 組合兩個檔案的標題
    combined_title = combine_titles(df1, df2, header_row1, header_col1, header_row2, header_col2)

    # 在這裡，你可以繼續進行其他操作，例如合併兩個檔案，執行相應的分析等

    # 範例：將組合後的標題寫入新的 Excel 檔案
    output_df = pd.DataFrame(columns=[combined_title])

    # 在這裡，你可以繼續進行其他操作，例如將兩個檔案的數據合併等

    # 去除重複的標題項目
    output_df = output_df.loc[:, ~output_df.columns.duplicated()]

    # 處理完成後返回處理後的數據
    return output_df


st.title('進行Excel抬頭列項目比對')

if st.checkbox('資料比對'):
    uploaded_file1 = st.file_uploader("請上傳Excel檔案一")
    if uploaded_file1 is not None:
        # To read file as bytes:
        uploaded_file2 = st.file_uploader("請上傳Excel檔案二")
        if uploaded_file2 is not None:
            bytes_data1 = uploaded_file1.getvalue()
            bytes_data2 = uploaded_file2.getvalue()
            result_byte_data = process_excel_data(bytes_data1,bytes_data2)
            st.download_button(
                label="Download data as Excel",
                data=result_byte_data,
                file_name='CombinedExcel.xlsx',
                mime='Excel/xlsx',
            )



