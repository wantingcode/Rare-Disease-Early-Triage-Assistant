# disease_mapper.py

def map_symptoms_to_diseases(matched_symptoms):
    """
    输入FAISS检索返回的Top3症状，映射到Top3疾病列表。
    
    参数:
        matched_symptoms (list): 每个元素是一个dict，包含症状描述和疾病信息。
    
    返回:
        diseases (list): 不重复的疾病英文名列表。
    """
    diseases = []
    for symptom_info in matched_symptoms:
        disease = symptom_info.get('disease_en')
        if disease and disease not in diseases:
            diseases.append(disease)
    return diseases

# 测试用
if __name__ == "__main__":
    sample_matched_symptoms = [
        {"matched_symptom": "皮肤和眼睛发黄", "disease_en": "Alagille Syndrome"},
        {"matched_symptom": "黄疸", "disease_en": "Alagille Syndrome"},
        {"matched_symptom": "生长缓慢", "disease_en": "Marfan Syndrome"}
    ]
    top_diseases = map_symptoms_to_diseases(sample_matched_symptoms)
    print(top_diseases)