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

patient_info_translation = {
    "患者姓名": "Patient Name",
    "患者类型": "Patient Category",
    "患者ID": "Patient ID",
    "检查时间": "Examination Time",
}


def extract_and_translate(excel_file, output_json):
    df = pd.read_excel(excel_file, dtype={"患者ID": str})
    category_translation = {
        "住院": "Inpatient",
        "门诊": "Outpatient"
    }
    df["患者类型"] = df["患者类型"].replace(category_translation)

    required_columns = list(patient_info_translation.keys())
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"缺少必要的列：{col}")

    rightmost_column = df.iloc[:, -1].dropna()
    data_list = rightmost_column.tolist()

    translated_data_list = []

    for i, data in enumerate(data_list):
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

        for cn_key, en_key in patient_info_translation.items():
            translated_data[en_key] = str(df.iloc[i][cn_key])  

        translated_data_list.append(translated_data)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(translated_data_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    extract_and_translate("work.xlsx", "Results.json")