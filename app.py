# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 22:28:54 2025

@author: user
"""


import dash 
import dash_core_components as dcc 
import joblib
from dash import Dash,html,dcc,Input, Output, State, callback
import pandas as pd
import numpy as np
from pathlib import Path
import os
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

rf_clf_load = joblib.load(os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl'))
# rf_clf_load = joblib.load(os.path.join("D:\GCP_VM_Fraud_Dashboard", 'random_forest_model.pkl'))
# os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')

columns = ['Area_南投市', 'Area_南投縣', 'Area_嘉義市', 'Area_嘉義縣', 'Area_基隆市', 'Area_宜蘭縣',
       'Area_屏東市', 'Area_屏東縣', 'Area_彰化縣', 'Area_新北市', 'Area_新竹市', 'Area_新竹縣',
       'Area_桃園市', 'Area_澎湖縣', 'Area_臺中市', 'Area_臺北市', 'Area_臺南市', 'Area_臺東市',
       'Area_臺東縣', 'Area_臺灣', 'Area_花蓮縣', 'Area_苗栗縣', 'Area_金門縣', 'Area_雲林縣',
       'Area_高雄市', 'Victim_Gender_F', 'Victim_Gender_M', 'Victim_Career_上班族',
       'Victim_Career_保全', 'Victim_Career_公務員', 'Victim_Career_其他',
       'Victim_Career_司機', 'Victim_Career_娛樂/藝術', 'Victim_Career_學生',
       'Victim_Career_家庭主婦', 'Victim_Career_工人', 'Victim_Career_工程師',
       'Victim_Career_技術工', 'Victim_Career_政治人物', 'Victim_Career_教育',
       'Victim_Career_會計', 'Victim_Career_服務業', 'Victim_Career_業務',
       'Victim_Career_法律', 'Victim_Career_無業', 'Victim_Career_科技業',
       'Victim_Career_自營商', 'Victim_Career_行政', 'Victim_Career_警察',
       'Victim_Career_軍人', 'Victim_Career_退休', 'Victim_Career_醫療',
       'Victim_Career_金融業', 'Victim_Age']


fraud_types = [
    '假中獎', '假交友', '假冒身分', '假投資', '假推銷', '假檢警', '假求職', 
    '假貸款', '宗教詐騙', '網購', '繳費詐騙', '色情應召', '遊戲', '釣魚簡訊', '騙取金融帳戶'
]

def input_vector(Area,Gender,Career,Age):

    # 你的輸入資料
    input_data = {"Area":Area,"Gender":Gender,"Career":Career,"Age":Age}

    # 初始化一個零值的 DataFrame
    data = np.zeros(len(columns), dtype=int)

    # 將資料轉換為對應的欄位索引並賦值為 1
    area_column = f"Area_{input_data['Area']}"
    gender_column = f"Victim_Gender_{input_data['Gender']}"
    career_column = f"Victim_Career_{input_data['Career']}"
    age_column = "Victim_Age"
    # platform_column = f"Platform_{input_data['Platform']}"

    # 找出對應欄位的索引
    area_idx = columns.index(area_column)
    gender_idx = columns.index(gender_column)
    career_idx = columns.index(career_column)
    age_idx = columns.index(age_column)
    # platform_idx = columns.index(platform_column)

    # 設定對應欄位的值為 1
    data[area_idx] = 1
    data[gender_idx] = 1
    data[career_idx] = 1
    # data[platform_idx] = 1
    data[age_idx] = input_data["Age"]

# age_column = "Victim_Age_"
# if age_column in columns:
#     age_idx = columns.index(age_column)
#     data[age_idx] = 1

# 轉換為 DataFrame
    df_result = pd.DataFrame([data], columns=columns)
    print(df_result)
    rf_clf_load.predict(df_result)[0]
    type_index = np.where(rf_clf_load.predict(df_result)[0]>=1)
    type_index = type_index[0].tolist()
    type_index
    result = np.array(fraud_types)[type_index].tolist()
    result = ','.join(result )
    return(result)


# input_vector('新北市','M','學生',18)






Career = ['上班族','保全','公務員','其他','司機','娛樂/藝術','學生','家庭主婦','工人','工程師','技術工','政治人物','教育','會計','服務業','業務','法律','無業','科技業','自營商','行政','警察','軍人','退休','醫療','金融業']
Area = ['南投市','南投縣','嘉義市','嘉義縣','基隆市','宜蘭縣','屏東市','屏東縣','彰化縣','新北市','新竹市','新竹縣','桃園市','澎湖縣','臺中市','臺北市','臺南市','臺東市','臺東縣','臺灣','花蓮縣','苗栗縣','金門縣','雲林縣','高雄市']
Gender =['女', '男']
app.layout = html.Div([ html.H2('Fraud_Dashboard'), 
                       
                       html.Label('"請選擇居住地":'),
                       dcc.Dropdown( id='dropdown_area', options=[{'label': i, 'value': i} for i in Area], value='臺北市', placeholder="請選擇居住地" ),
                       html.Label('"請選擇職業":'),
                       dcc.Dropdown( id='dropdown_career', options=[{'label': i, 'value': i} for i in Career], value='學生', placeholder="請選擇職業" ),
                       html.Label('"請選擇性別:'),
                       dcc.Dropdown( id='dropdown_gender', options=[{'label': i, 'value': j} for i,j in zip(Gender,['F','M'])], value='F', placeholder="請選擇性別" ),
                       html.Label('"請輸入年齡:'),
                       dcc.Input(id="age" ,type="number",
                                 min=0,  # 設定最小值
                                 max=120,  # 設定最大值, 
                                 placeholder="請輸入年齡", style={'marginRight':'10px'}, value=18),
                       html.Div(id='pre_type_result')
                       ]

                      
                      
                      
                      )

@app.callback(Output('pre_type_result', 'children'), 
              [Input('dropdown_area', 'value'),
               Input('dropdown_career', 'value'),
               Input('dropdown_gender', 'value'),
               Input('age', 'value')]) 
def predict_victim_type(Area,Career,Gender,Age): 
    result = input_vector(Area,Gender,Career,Age)  
    output = "無匹配可能詐騙類型" if result == "" else result
    show = html.Div([html.Label('高機率詐騙類型'),html.Div(output)])
    
    return show

if __name__ == '__main__': 
    app.run_server(host='0.0.0.0', port=8085) #host='0.0.0.0', port=8085
