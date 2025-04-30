import json

def load_symptom_knowledge():
    with open('symptom_mapping_top50.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # data是dict，不是list！

    mapping = {}
    for item in data:  # 正确遍历疾病列表
        disease = item['disease_en']
        primary = item.get('primary', [])
        secondary = item.get('secondary', [])
        mapping[disease] = {
            "primary": primary,
            "secondary": secondary
        }
    return mapping

class SymptomDiseaseMapper:
    def __init__(self, mapping_path):
        # 加载症状到疾病的映射表
        with open(mapping_path, 'r', encoding='utf-8') as f:
            self.symptom_mapping = json.load(f)
    
    def get_disease_info(self, symptom_text):
        """
        根据症状文本返回对应的疾病信息。
        """
        return self.symptom_mapping.get(symptom_text, {})

    def list_all_symptoms(self):
        """
        列出所有支持的症状文本。
        """
        return list(self.symptom_mapping.keys())

# 使用示例（测试用）
if __name__ == "__main__":
    mapper = SymptomDiseaseMapper(
        mapping_path="symptom_mapping_top20.json"
    )
    symptom = "皮肤和眼睛发黄（黄疸）"
    info = mapper.get_disease_info(symptom)
    print(info)