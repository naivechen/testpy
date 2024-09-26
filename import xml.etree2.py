import xml.etree.ElementTree as ET
import numpy as np
from sklearn.naive_bayes import GaussianNB

# 将XML文件转换为字典格式
def xml_to_dict(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'hl7': 'urn:hl7-org:v3'}
    
    data = {}
    code_elem = root.find('hl7:code', ns)
    if code_elem is not None:
        data['心电图检查代码'] = code_elem.get('code')
        data['编码系统'] = code_elem.get('codeSystemName')

    effective_time_elem = root.find('hl7:effectiveTime/hl7:center', ns)
    if effective_time_elem is not None:
        data['观察时间'] = effective_time_elem.get('value')

    return data

# 使用贝叶斯分类器对数据进行分类
def classify_data(data):
    # 提取特征：心电图检查代码和编码系统的长度
    features = np.array([[len(data['心电图检查代码']), len(data['编码系统'])]])
    
    # 伪训练数据和标签
    X_train = np.array([[10, 5], [12, 4], [8, 6], [9, 3], [11, 5]])  # 示例特征
    y_train = np.array([0, 1, 0, 1, 0])  # 示例标签（0和1）

    # 创建和训练贝叶斯分类器
    model = GaussianNB()
    model.fit(X_train, y_train)

    # 进行预测
    prediction = model.predict(features)
    
    # 预测结果
    print(f"预测结果: {prediction[0]}")  # 预测结果


xml_file_path = 'D:\\下载\\吴洪涛202408141734.aECG.fda.xml'
data = xml_to_dict(xml_file_path)  # 转换XML文件为字典
print(data)  # 打印提取的数据

# 进行分类
classify_data(data)  # 对数据进行分类

