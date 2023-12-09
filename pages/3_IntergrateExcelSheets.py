import streamlit as st
import pandas as pd

# 定義 Streamlit 畫面
st.title('Combine Excel Sheets')

# 讓使用者上傳 Excel 檔案
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# 如果有上傳檔案
if uploaded_file is not None:
    # 讀取 Excel 文件
    xls = pd.ExcelFile(uploaded_file)

    # 創建一個新的 Excel 文件
    # output_excel = pd.ExcelWriter('combined_output.xlsx', engine='xlsxwriter')
    output_df = pd.DataFrame(columns=column_differences)
    output_excel = BytesIO()
   
    # 遍歷每個 SHEET
    all_sheets = []
    for sheet_name in xls.sheet_names:
        # 讀取 SHEET 的資料
        df = pd.read_excel(xls, sheet_name)
        all_sheets.append(df)

    # 將所有 SHEET 合併到同一個新的 SHEET
    combined_df = pd.concat(all_sheets, ignore_index=True)
    # 將合併後的結果寫入新的 Excel 檔案
    combined_df.to_excel(output_excel, sheet_name='Combined_Sheets', index=False, engine='openpyxl')
    output_excel_data = output_excel.getvalue()
    # 保存新的 Excel 文件
    #output_excel.save()
    # 提供下載連結
    st.download_button(
    label="Download data as Excel",
    data=output_excel_data,
    file_name='CombinedExcel.xlsx',
    mime='Excel/xlsx',
    )