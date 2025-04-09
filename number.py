import pandas as pd
import json
import re


translation_map = {
    "TAPSE": "TAPSE",
    "主动脉窦部内径": "Aortic Sinus Diameter",
    "左房内径": "Left Atrial Diameter",
    "左房容积指数": "Left Atrial Volume Index",
    "室间隔厚度": "Interventricular Septum Thickness",
    "左室舒张末期内径": "Left Ventricular End-Diastolic Diameter",
    "左室后壁厚度": "Left Ventricular Posterior Wall Thickness",
    "左室收缩末期内径": "Left Ventricular End-Systolic Diameter",
    "EF": "Ejection Fraction",
    "窦部内径": "Sinus Diameter",
    "右房内径（横径）": "Right Atrial Diameter (Horizontal)",
    "右室内径（横径）": "Right Ventricular Diameter (Horizontal)",
    "二尖瓣E峰": "Mitral E-wave Velocity",
    "二尖瓣A峰": "Mitral A-wave Velocity",
    "E/A": "E/A Ratio",
    "EDT": "E-wave Deceleration Time",
    "间隔e'": "Septal e' Velocity",
    "侧壁e'": "Lateral e' Velocity",
    "E/e'": "E/e' Ratio",
    "肺动脉压收缩压": "Pulmonary Arterial Systolic Pressure",
    "主动脉瓣环内径": "Aortic Valve Annulus Diameter",
    "窦管内径": "Sinotubular Junction Diameter",
    "远端最宽径": "Maximum Distal Diameter",
    "RV面积改变分数": "RV Area Change Fraction",
    "TDI三尖瓣环s'": "TDI Tricuspid Annular s' Velocity",
    "平均e'": "Average e' Velocity"
}
excel_file = 'work.xlsx'
df = pd.read_excel(excel_file)
rightmost_column = df.iloc[:, -1].dropna()
data_list = rightmost_column.tolist()

translated_data_list = []
for data in data_list:
    translated_data = {}
    for item in data.split(','):
        if ':' not in item:
            continue

        key, value = item.split(':', 1)

        key = key.replace('′', "'").replace('‘', "'").replace('’', "'").strip()

        english_key = translation_map.get(key, key)

        match = re.search(r'\d+\.?\d*', value)
        if match:
            num_str = match.group()
            value = float(num_str) if '.' in num_str else int(num_str)
        else:
            value = None

        translated_data[english_key] = value

    translated_data_list.append(translated_data)

json_file = 'Results.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(translated_data_list, f, ensure_ascii=False, indent=4)



md_content = {
    "TAPSE": "三尖瓣环运动幅度",
    "Aortic Sinus Diameter": "主动脉窦部内径",
    "Left Atrial Diameter": "左房内径",
    "Interventricular Septum Thickness": "室间隔厚度",
    "Left Ventricular End-Diastolic Diameter": "左室舒张末期内径",
    "Left Ventricular Posterior Wall Thickness": "左室后壁厚度",
    "Left Ventricular End-Systolic Diameter": "左室收缩末期内径",
    "Ejection Fraction": "射血分数",
    "Right Atrial Diameter (Horizontal)": "右房内径（横径）",
    "Right Ventricular Diameter (Horizontal)": "右室内径（横径）",
    "Mitral E-wave Velocity": "二尖瓣E峰,",
    "Mitral A-wave Velocity": "二尖瓣A峰",
    "E/A Ratio": "二尖瓣E峰与A峰速度比值",
    "E-wave Deceleration Time": "舒张时间指二尖瓣舒张的时间长度",
    "Septal e' Velocity": "心脏间隔部位的早期舒张速度",
    "Lateral e' Velocity": "心脏侧壁部位的早期舒张速度",
    "E/e' Ratio": "二尖瓣E峰与间隔e'的比值",
    "Pulmonary Arterial Systolic Pressure": "肺动脉压收缩压",
    "Aortic Valve Annulus Diameter": "主动脉瓣环内径",
    "Sinotubular Junction Diameter": "窦管内径",
    "Maximum Distal Diameter": "远端最宽径",
    "RV Area Change Fraction": "RV面积改变分数",
    "TDI Tricuspid Annular s' Velocity": "三尖瓣环的运动速度",
    "Average e' Velocity": "心脏各部位e'速度的平均值",
    "Left Atrial Diameter": "左房内径",
    "Sinus Diameter": "窦部内径",

}
max_eng_len = max(len(eng) for eng in md_content.keys())
max_chi_len = max(len(chi) for chi in md_content.values())
md_file = 'parameters_description.md'

with open(md_file, 'w', encoding='utf-8') as f:
    f.write(f"| {'ENGLISH'.ljust(max_eng_len)} | {'CHINISE'.ljust(max_chi_len)} |\n")
    f.write(f"|{'-' * (max_eng_len + 2)}|{'-' * (max_chi_len + 2)}|\n")
 
    for eng, chi in md_content.items():
        f.write(f"| {eng.ljust(max_eng_len)} | {chi.ljust(max_chi_len)} |\n")
