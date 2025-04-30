# diagnosis_engine.py

from symptom_mapping_loader import load_symptom_knowledge

# 加载症状知识库
symptom_knowledge = load_symptom_knowledge()

def score_diseases(candidates, user_answers):
    """
    根据用户回答（yes/no）对每个候选疾病打分。
    
    :param candidates: 疾病英文名或中文名列表
    :param user_answers: 用户回答的症状字典 {"症状": "yes"/"no"}
    :return: List of (disease, score)，按得分降序排序
    """
    scores = {}

    for disease in candidates:
        score = 0
        disease_symptoms = symptom_knowledge.get(disease, {})
        for level, weight in [("primary", 3), ("secondary", 1)]:
            for symptom in disease_symptoms.get(level, []):
                answer = user_answers.get(symptom)
                if answer == "yes":
                    score += weight
        scores[disease] = score

    sorted_diseases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_diseases

def get_top_disease(scored_diseases):
    """
    从打分结果中选出得分最高的Top1疾病。
    """
    if scored_diseases:
        return scored_diseases[0][0]
    return None

# 测试代码（可删除）
if __name__ == "__main__":
    candidates = ["Alagille Syndrome", "Marfan Syndrome"]
    answers = {
        "皮肤发黄": "yes",
        "骨骼异常": "no",
        "胆汁淤积": "yes"
    }
    results = score_diseases(candidates, answers)
    print("打分结果:", results)
    print("Top1 疾病:", get_top_disease(results))