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
