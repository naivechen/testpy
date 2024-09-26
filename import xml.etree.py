import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file):
    # 加载XML文件
    tree = ET.parse(xml_file)  
    root = tree.getroot()

    # 命名空间
    ns = {'hl7': 'urn:hl7-org:v3'}

    # 创建一个字典来存储提取的数据
    data = {}

    # 提取心电图检查代码
    code_elem = root.find('hl7:code', ns)
    if code_elem is not None:
        data['心电图检查代码'] = code_elem.get('code')
        data['编码系统'] = code_elem.get('codeSystemName')

    # 提取观察时间
    effective_time_elem = root.find('hl7:effectiveTime/hl7:center', ns)
    if effective_time_elem is not None:
        data['观察时间'] = effective_time_elem.get('value')

    # 提取所有元素的标签和内容
    data['所有元素'] = []
    for elem in root.iter():
        data['所有元素'].append({'标签': elem.tag, '内容': elem.text})

    # 返回JSON格式
    return json.dumps(data, ensure_ascii=False, indent=4)


xml_file_path = 'D:\\下载\\吴洪涛202408141734.aECG.fda.xml'
json_output = xml_to_json(xml_file_path)
print(json_output)
