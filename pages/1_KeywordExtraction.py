import time

import streamlit as st

import numpy as np
import pandas as pd
import re
from io import BytesIO

def extract_key_points(data):
    # 使用正規表達式擷取要點
    pattern = r'[\u4e00-\u9fa5a-zA-Z\s]+[:：]'
    key_points_match = re.findall(pattern, data)

    # 去除符號，保留純文字要點
    key_points = [re.sub(r'[:：]', '', match) for match in key_points_match]

    return key_points


def clean_columns(columns):
    # 去除包含 "Unnamed" 的欄位
    cleaned_columns = [col for col in columns if 'Unnamed' not in col]
    return cleaned_columns

def find_header_location(df):
    # 尋找標題所在的位置，這裡簡單示範在每行每列中找到第一個不為空的單元格作為標題位置
    for index, row in df.iterrows():
        for col_index, value in enumerate(row):
            if pd.notna(value):
                return index, col_index
    return None, None

def combine_headers(df1, df2):
    # 獲取第一個檔案的所有 columns
    columns1 = df1.columns.tolist()

    # 獲取第二個檔案的所有 columns
    columns2 = df2.columns.tolist()

    # 組合兩個檔案的 columns，確保沒有重複的標頭內容
    combined_columns = list(set(columns1 + columns2))

    return combined_columns

def find_column_differences(df1, df2):
    # 獲取第一個檔案的所有 columns
    columns1 = set(clean_columns(df1.columns))

    # 獲取第二個檔案的所有 columns
    columns2 = set(clean_columns(df2.columns))

    # 找出兩個檔案的 columns 中的差異
    differences = columns2 - columns1

    return list(differences)

def process_excel_data(byte_data):
    # 讀取 Excel 檔案
    df= pd.read_excel(BytesIO(byte_data), engine='openpyxl')

   
    # 提取最後一欄的資料
    last_column = df.iloc[:, -1]

    # 針對每個要點進行擷取，並插入新的欄位
    extracted_key_points = last_column.apply(extract_key_points)
    df['Extracted_Key_Points'] = extracted_key_points

    # 在這裡，你可以繼續進行其他操作，例如合併兩個檔案，執行相應的分析等

    # 範例：將組合後的標題寫入新的 Excel 檔案
    
    # 在這裡，你可以繼續進行其他操作，例如將兩個檔案的數據合併等

    # 去除重複的標題項目
   # output_df = output_df.loc[:, ~output_df.columns.duplicated()]

    output_excel = BytesIO()
    df.to_excel(output_excel, index=False, engine='openpyxl')

    # 取得最終的二進制數據
    output_excel_data = output_excel.getvalue()

    # 處理完成後返回處理後的數據
    return output_excel_data


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



