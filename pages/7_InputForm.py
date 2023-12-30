import streamlit as st
import sqlite3
from datetime import datetime

# 初始化SQLite連接
conn = sqlite3.connect('nutrition_records.db')
c = conn.cursor()
# 用於計算的函數
def calculate_calorie_protein_needs(weight, factor, is_protein=False):
    if is_protein:
        return weight * factor  # 蛋白質需求計算
    else:
        return weight * factor  # 熱量需求計算

# 創建表格（如果不存在）
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS nutrition_records (
        date TEXT, 
        service_time TEXT, 
        consultation_method TEXT, 
        discussion_reason TEXT,
        other_discussion_reason TEXT,
        diet_orientation TEXT,
        current_eating_method TEXT,
        diet_principle TEXT,
        other_diet_principle TEXT,
        diet_texture TEXT,
        health_supplements TEXT,
        other_health_supplement TEXT,
        special_nutrition_products TEXT,
        other_special_nutrition_product TEXT
        )''')

create_table()
# 營養紀錄表輸入介面 表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# 應用標題

tab1, tab2 ,tab3 ,tab4 ,tab5, tab6, tab7= st.tabs(["營養紀錄表", "PG-SGA","營養評估","營養診斷","營養介入","營養品補助專區","營養評值"])
with tab1:
    tab1.title('營養紀錄表輸入介面')
    # 使用columns來創建多列佈局
    col1, col2 = tab1.columns(2)
    # 輸入表單
    with col1:
        # 日期選擇
        date = st.date_input('日期')
        
        # 服務時間下拉選單
        service_time = st.selectbox('服務時間', ['上午', '下午', '晚上'])

        # 諮詢方式下拉選單
        consultation_method = st.selectbox('諮詢方式', ['面對面', '視訊', '電話'])
    with col2:
        # 會談原因單選
        discussion_reason_options = ['營養諮詢', '營養品補助']
        discussion_reason = st.radio('會談原因', discussion_reason_options)
        # "其他"選項的checkbox和文本輸入
        other_discussion_reason_check = st.toggle('其他目的')
        if other_discussion_reason_check:
            discussion_reason='其他目的'
            other_discussion_reason = st.text_input('請說明其他會談原因')  

        # 飲食方向多選
    diet_orientation = tab1.multiselect('飲食方向', ['治療期間飲食調整', '副作用飲食對策', '飲食迷思', '營養品選購/使用', '腸胃道手術後飲食', '康復期飲食'])

        # 現在進食方式多選
    current_eating_method = tab1.multiselect('現在進食方式', ['由口進食', '鼻胃管灌食', '胃造口灌食', '腸造口灌食', '周邊靜脈營養', '全靜脈營養'])

        # 飲食原則單選
    diet_principle = tab1.radio('飲食原則', ['均衡飲食', '高熱量高蛋白飲食', '糖尿病飲食', '低渣飲食', '高纖飲食', '素食', '透析飲食', '慢性腎衰竭飲食', '肝病飲食', '其他'])
    other_diet_principle = tab1.toggle('其他飲食原則')
    if other_diet_principle:
        other_diet_info = tab1.text_input('請說明其他飲食原則')  
        # 飲食質地多選
    diet_texture = tab1.multiselect('飲食質地', ['普通飲食', '軟質飲食', '細碎飲食', '半流質飲食', '全流質飲食', '清流質飲食', '管灌飲食'])

        # 保健食品多選
    health_supplements = tab1.multiselect('保健食品', ['維生素類', '礦物質類', '魚油/藻油', '益生菌/益生質/益生元', '中草藥萃取(如:中藥、薑黃、蔓越莓等)', '蔘類', '藻類', '菇菌類(如:靈芝、牛樟芝)', '植化素'])
    other_health_supplement = tab1.toggle('其他保健食品')
    if other_health_supplement:
        other_health_info = tab1.text_input('請說明其他保健食品')  
        # 特殊營養品多選
    special_nutrition_products = tab1.multiselect('特殊營養品', ['均衡配方', '腫瘤配方', '糖尿病配方', '濃縮配方', '透析前配方', '透析後配方', '肺病配方', '麩醯胺酸', '蛋白粉'])
    other_special_nutrition_product = tab1.toggle('其他特殊營養品')
    if other_special_nutrition_product:
        other_special_nutrition_info = tab1.text_input('請說明其他特殊營養品')  

    submit_button = tab1.button (label='提交')

    # 處理表單提交
    if submit_button:
        # 將數據添加到SQLite資料庫
        c.execute('''INSERT INTO nutrition_records (
            date, service_time, consultation_method, discussion_reason, other_discussion_reason,
            diet_orientation, current_eating_method, diet_principle, other_diet_principle,
            diet_texture, health_supplements, other_health_supplement,
            special_nutrition_products, other_special_nutrition_product) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (date, service_time, consultation_method, discussion_reason, other_discussion_reason,
            ','.join(diet_orientation), ','.join(current_eating_method), diet_principle, other_diet_principle,
            ','.join(diet_texture), ','.join(health_supplements), other_health_supplement, ','.join(special_nutrition_products), other_special_nutrition_product))
        conn.commit()
        tab1.success('資料已提交！')
# PG-SGA 表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab2:
    tab2.header("PG-SGA")
    colt2_1, colt2_2 = tab2.columns(2)
    # 體重變化部分
    with colt2_1:
        tab2.subheader("(1) 體重變化")
        height = colt2_1.number_input("身高 (cm)", min_value=100, max_value=200)
        current_weight = colt2_1.number_input("目前體重 (kg)", min_value=0, max_value=150)
    with colt2_2:
        # Calculate BMI
        bmi = current_weight / ((height / 100) ** 2)
        colt2_2.text("BMI: %.2f" % bmi)
        # Determine body shape based on BMI
        if bmi < 18.5:
            body_shape = "體重過輕"
        elif bmi < 24:
            body_shape = "正常體重"
        elif bmi < 27:
            body_shape = "超重"
        else:
            body_shape = "肥胖"
        colt2_2.text("體型: %s" % body_shape)
        # Calculate ideal weight based on man and Woman height
        man_ideal_weight = (height - 170) * 0.6 + 62
        woman_ideal_weight = (height - 158) * 0.5 + 52
        colt2_2.text("理想體重:男 %.2f  公斤, 女 %.2f 公斤" % (man_ideal_weight, woman_ideal_weight))

        # Display adjustment weight if BMI >= 24
        if bmi >= 24:
            man_adjustment_weight = current_weight - man_ideal_weight
            woman_adjustment_weight = current_weight - woman_ideal_weight
            colt2_2.text("調整體重:男 %.2f  公斤, 女 %.2f 公斤" % (man_adjustment_weight, woman_adjustment_weight))


    one_month_ago_weight = tab2.number_input("1個月前體重 (kg)", min_value=0, max_value=150)
    if one_month_ago_weight > 0:
        tab2.text("1個月前體重變化率: %.2f %%" % ((current_weight - one_month_ago_weight) / one_month_ago_weight * 100))
    six_months_ago_weight = tab2.number_input("6個月前體重 (kg)", min_value=0, max_value=150)
    if six_months_ago_weight > 0:
        tab2.text("6個月前體重變化率: %.2f %%" % ((current_weight - six_months_ago_weight) / six_months_ago_weight * 100))
    weight_change_last_two_weeks = tab2.radio("過去兩星期體重變化", ["減少", "維持", "增加"])

    # 飲食情況部分
    tab2.subheader("(2) 飲食情況")
    eating_comparison = tab2.radio("最近一個月與過去進食量相比", ["沒有改變", "比之前多", "比之前少"])
    current_food_type = tab2.radio("我目前吃的食物類型", ["比平常少量一點的一般食物", "只能吃一點固體食物", "只能吃流質", "大部分都喝營養品", "吃非常少的任何食物", "管灌或靜脈營養"])

    # 副作用部分
    tab2.subheader("(3) 副作用")
    symptoms = {
    '沒有飲食方面的問題': 0,
    '沒有食欲，就是不想吃':3,
    '嘔吐':3,
    '噁心':1,
    '腹瀉':3,
    '便祕':1,
    '口乾':1,
    '口腔潰瘍':2,
    '有怪味困擾我':1,
    '吃起來感覺沒有味道，或味道覺得奇怪':1,
    '感覺比較快飽':1,
    '吞嚥困難':2,
    '疲倦':1,
    '疼痛':3,
    '其他(抑鬱、金錢或牙齒問題)':1,
    # 其他症狀按照圖片中的分數添加
    }
    side_effects = tab2.multiselect("過去兩周有出現哪些副作用，導致無法攝取足夠的營養",list(symptoms.keys()))
    if "疼痛" in side_effects:
        other_pain_position = tab2.text_input("請說明疼痛位置")
    if "其他(抑鬱、金錢或牙齒問題)" in side_effects:
        other_side_effects = tab2.text_input("請說明其他的副作用")

    # 活動與功能部分
    tab2.subheader("(4) 活動與功能")
    activity_status = tab2.radio("過去一個月活動狀態",
                                ["正常無限制", "不如平常，但日常生活起居還能自我料理", "大部分時間躺或坐", "幾乎整天都在床或椅子上", "幾乎一直臥床"])

    # 計算分數

    # 體重變化百分比計算
    weight_change_percentage = 0
    weight_change_percentage_in_sixmonth = 0
    if one_month_ago_weight > 0:
        weight_change_percentage = ((current_weight - one_month_ago_weight) / one_month_ago_weight) * 100
    elif six_months_ago_weight > 0:
        weight_change_percentage_in_sixmonth = ((current_weight - six_months_ago_weight) / six_months_ago_weight) * 100
    # 根據百分比決定分數

    weight_score = 0
    if weight_change_percentage >= 10:
        weight_score = 4
    elif weight_change_percentage >= 5.0:
        weight_score = 3
    elif weight_change_percentage >= 3.0:
        weight_score = 2
    elif weight_change_percentage >= 2.0:
        weight_score = 1
    elif weight_change_percentage == 0:
        if weight_change_percentage_in_sixmonth >= 20:
            weight_score = 4    
        elif weight_change_percentage_in_sixmonth >= 10.0:
            weight_score = 3    
        elif weight_change_percentage_in_sixmonth >= 6.0:
            weight_score = 2
        elif weight_change_percentage_in_sixmonth >= 2.0:
            weight_score = 1

    weight_score += 1 if weight_change_last_two_weeks == '減少' else 0
    # 食物攝入分數計算
    food_intake_score = 0
    if eating_comparison == '比之前少':
        food_intake_score = 1
    elif eating_comparison == '比之前多':
        food_intake_score = 0
    else: # '正常'
        food_intake_score = 0
    # 根据食物类型给分["比平常少量一點的一般食物", "只能吃一點固體食物", "只能吃流質", "大部分都喝營養品", "吃非常少的任何食物", "管灌或靜脈營養"]
    food_type_score = 0
    if current_food_type == '比平常少量一點的一般食物':
        food_type_score = 1
    elif current_food_type == '只能吃一點固體食物':
        food_type_score = 2
    elif current_food_type == '只能吃流質':
        food_type_score = 3
    elif current_food_type == '大部分都喝營養品':
        food_type_score = 3
    elif current_food_type == '吃非常少的任何食物':
        food_type_score = 4
    elif current_food_type == '管灌或靜脈營養':
        food_type_score = 0
    # 取最高分
    food_intake_total_score = max(food_intake_score, food_type_score)

    # 症狀分數計算
    symptoms_score = sum(symptoms[symptom] for symptom in side_effects)

    # 活動與功能分數計算 ["正常無限制", "不如平常，但日常生活起居還能自我料理", "大部分時間躺或坐", "幾乎整天都在床或椅子上", "幾乎一直臥床"]
    activity_scores = {
        '正常無限制': 0,
        '不如平常，但日常生活起居還能自我料理': 1,
        '大部分時間躺或坐': 2,
        '幾乎整天都在床或椅子上': 3,
        '幾乎一直臥床': 3,
    }
    activity_score = activity_scores[activity_status]

    # 總分計算
    total_score = weight_score + food_intake_total_score + symptoms_score + activity_score

    # 顯示結果
    tab2.subheader('PG-SGA總分')
    tab2.write(f'您的PG-SGA總分是: {total_score}')
# 營養評估 表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab3:
        
    tab3.header("營養評估")

    # 個案主訴
    case_complaint = tab3.text_area("個案主訴")

    # 個案提問
    case_question = tab3.text_area("個案提問")

    # 飲食來源單選
    diet_source = tab3.radio("飲食來源", ["自己", "配偶", "子女", "其他親友", "外傭", "接受送餐"],)

    # 飲食內容
    diet_content = tab3.text_area("飲食內容")

    # 攝取量計算
    tab3.subheader("攝取量計算")
    # 這裡可以添加更多有關攝取量計算的字段
    # 示例：全榖雜糧類、豆魚蛋肉類(中脂)、蔬菜類的攝取量
    tab3.write("(1)六大類食物")
    colt3_1, colt3_2,colt3_3= tab3.columns(3)
    with colt3_1:
        whole_grains = colt3_1.number_input("全榖雜糧類攝取量", min_value=0, max_value=30)
        protein = colt3_1.number_input("豆魚蛋肉類(中脂)攝取量", min_value=0, max_value=30)
    with colt3_2:
        vegetables = colt3_2.number_input("蔬菜類攝取量", min_value=0, max_value=30)
        fruits = colt3_2.number_input("水果類攝取量", min_value=0, max_value=30)
    with colt3_3:
        dairy = colt3_3.number_input("乳製品類攝取量", min_value=0, max_value=30)
        fats = colt3_3.number_input("油脂類攝取量", min_value=0, max_value=30)
    tab3.write("(2) 包裝食品")
    colt3_4, colt3_5,colt3_6= tab3.columns(3)
    with colt3_4:
        carbs = colt3_4.number_input("碳水化合物攝取量 (克)", min_value=0, max_value=500, step=1)
    with colt3_5:
        protein_packaged = colt3_5.number_input("蛋白質攝取量 (克)", min_value=0, max_value=200, step=1)
    with colt3_6:
        fat = colt3_6.number_input("脂肪攝取量 (克)", min_value=0, max_value=120, step=1)

    # 營養品部分
    tab3.write("(3) 營養品")
    colt3_7, colt3_8,colt3_9= tab3.columns(3)
    with colt3_7:
        Nutritional_1 = colt3_7.number_input("倍力素", min_value=0.0, max_value=20.0)
        Nutritional_2 = colt3_7.number_input("飲沛癌症專用",  min_value=0.0, max_value=20.0)
        Nutritional_3 = colt3_7.number_input("完膳腫瘤配方", min_value=0.0, max_value=20.0)
        Nutritional_4 = colt3_7.number_input("均衡配方(如:原味安素、益力壯17)",  min_value=0.0, max_value=20.0)
        Nutritional_5 = colt3_7.number_input("安素雙卡",  min_value=0.0, max_value=20.0)
    with colt3_8:
        Nutritional_6 = colt3_8.number_input("倍速", min_value=0.0, max_value=20.0)
        Nutritional_7 = colt3_8.number_input("補體素倍力",  min_value=0.0, max_value=20.0)
        Nutritional_8 = colt3_8.number_input("益力壯高效魚油優蛋白配方", min_value=0.0, max_value=20.0)
        Nutritional_9 = colt3_8.number_input("糖尿配方(不包含葡勝納嚴選)",  min_value=0.0, max_value=20.0)
    with colt3_9:
        Nutritional_9 = colt3_9.number_input("碳水化合物",min_value=0.0, max_value=500.0)
        Nutritional_10 = colt3_9.number_input("蛋白質", min_value=0.0, max_value=200.0)
        Nutritional_11 = colt3_9.number_input("脂肪", min_value=0.0, max_value=120.0)
    # 應用標題
    tab3.title('營養需求計算')

    # 輸入體重和選擇係數
    colt3_10, colt3_11= tab3.columns(2)
    #tab3.write("熱量需求")
    selected_weight1 = colt3_10.radio("熱量需求體重", ["現在體重", "理想體重", "調整體重"])
    calorie_factor = colt3_11.selectbox('熱量需求係數', [20, 25, 30, 35, 40])
    #t0ab3.write("蛋白質需求")
    selected_weight2 = colt3_10.radio("蛋白質體重", ["現在體重", "理想體重", "調整體重"])
    protein_factor = colt3_11.selectbox('蛋白質需求係數', [0.8, 1.0, 1.3, 1.5, 1.8, 2.0, 2.2, 2.5])

    # 執行計算
    if selected_weight1 == '現在體重':
        weight1 = current_weight
    elif selected_weight1 == '理想體重':
        weight1 = man_ideal_weight
    elif selected_weight1 == '調整體重':
        weight1 = man_adjustment_weight
    calorie_needs = calculate_calorie_protein_needs(weight1, calorie_factor)
    if selected_weight2 == '現在體重':
        weight2 = current_weight
    elif selected_weight2 == '理想體重':
        weight2 = man_ideal_weight
    elif selected_weight2 == '調整體重':
        weight2 = man_adjustment_weight
    protein_needs = calculate_calorie_protein_needs(weight2, protein_factor, is_protein=True)

    # 顯示結果
    tab3.write(f'熱量需求: {calorie_needs} kcal')
    tab3.write(f'蛋白質需求: {protein_needs} g')

    # 實際攝取量輸入
    actual_calorie_intake = tab3.number_input('實際攝取熱量 (kcal)', min_value=0.0)
    actual_protein_intake = tab3.number_input('實際攝取蛋白質 (g)', min_value=0.0)

    # 計算攝取百分比
    calorie_intake_percentage = (actual_calorie_intake / calorie_needs) * 100 if calorie_needs else 0
    protein_intake_percentage = (actual_protein_intake / protein_needs) * 100 if protein_needs else 0

    # 顯示攝取百分比
    tab3.write(f'熱量攝取百分比: {calorie_intake_percentage:.2f}%')
    tab3.write(f'蛋白質攝取百分比: {protein_intake_percentage:.2f}%')
# 營養診斷 表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab4:
    tab4.header("營養診斷")
    # 營養問題多選
    nutrition_problems = tab4.multiselect("營養問題 (選擇 0-3 個)",
                                        ["問題1", "問題2", "問題3", "問題4", "問題5"])
    # 病因問題輸入
    nutrition_problem_rootcause = tab4.text_input("請輸入病因(文字)")
    nutrition_problem_symptoms = tab4.text_input("請輸入症狀/徵候")

    # 提交按鈕
    submit_diagnosis_button = tab4.button(label='提交營養診斷')
# 營養介入表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab5:
    tab5.header("營養介入")
    # 飲食原則單選
    tab5.subheader("飲食原則")
    if diet_principle == "其他" :
        tab5.text(other_diet_principle )
    else:
        tab5.text(diet_principle)   

    # 飲食質地多選
    tab5.subheader ("飲食質地")
    tab5.text(diet_texture) 

    # 保健食品多選
    tab5.subheader ("保健食品")
    if other_health_supplement == True :
        tab5.text(other_health_info)
    else:    
        tab5.text(health_supplements)   


    # 特殊營養品多選
    tab5.subheader ("特殊營養品")
    if other_special_nutrition_product == True :
        tab5.text(other_special_nutrition_info)
    else:    
        tab5.text(special_nutrition_products)

    # 營養衛教內容
    nutrition_education_content = tab5.text_area("營養衛教內容")

    # 提交按鈕
    submit_button = tab5.button(label='提交營養介入')
# 營養介入表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab6:
    tab6.header("營養品補助專區")

    # 申請日期
    application_date = tab6.date_input("申請日期", datetime.today())

    # 轉介單位
    referral_unit = tab6.text_input("轉介單位")

    # 主要聯絡人
    primary_contact = tab6.text_input("主要聯絡人")

    # 收件人選擇
    recipient_options = ["個案", "其他"]
    recipient = tab6.radio("收件人", recipient_options)
    other_recipient = tab6.text_input("其他收件人") if recipient == "其他" else ""

    # 收件地址選擇
    address_options = ["同基本資料", "其他"]
    address = tab6.radio("收件地址", address_options)
    other_address = tab6.text_input("其他收件地址") if address == "其他" else ""

    # 補助階段
    subsidy_stage = tab6.radio("補助階段", ["初評", "追蹤", "超額", "結案"])

    # 是否給予補助
    subsidy_given = tab6.radio("是否給予補助", ["是", "否", "結案"])
    subsidy_reason = tab6.text_input("不給予補助原因") if subsidy_given == "否" else ""

    # 補助品項及數量
    supplement_items = tab6.text_area("補助品項及數量")

    # 營養品建議使用方式
    supplement_usage = tab6.text_area("營養品建議使用方式")

    # 提交按鈕
    submit_button = tab6.button(label='提交營養品補助信息')

    # 處理表單提交
    if submit_button:
        tab6.success('營養品補助信息已提交！')
        # 這裡可以添加將數據保存到資料庫的代碼
# 營養評值表格開始-----------------------------------------------------------------------
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
# ------------------------------------------------------------------------------------- 
with tab7:
    tab7.header("營養評值")

    # 建議追蹤選項
    follow_up_recommendation = tab7.radio("建議追蹤", ["是", "不需要"])
    if follow_up_recommendation == "是":
        follow_up_period = tab7.radio("追蹤周期", ["2週", "1個月", "3個月"])

    # 下次追蹤時間
    next_follow_up_date = tab7.date_input("下次追蹤時間", datetime.today())

    # 其他備註
    other_remarks = tab7.text_area("其他備註")

    # 附件檔案上傳
    uploaded_files = tab7.file_uploader("附件檔案", accept_multiple_files=True)

    # 提交按鈕
    submit_button = tab7.button(label='提交營養評值')
    # 處理表單提交
    if submit_button:
        tab7.success('營養評值已提交！')
# 關閉資料庫連接
conn.close()