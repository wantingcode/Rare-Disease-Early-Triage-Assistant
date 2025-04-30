# hospital_recommender.py
print("🟢 hospital_recommender.py 加载成功！find_hospitals(disease, user_country)")
import json

## 加载医院数据库
with open('hospitals_database.json', 'r', encoding='utf-8') as f:
    hospitals_data = json.load(f)

def find_hospitals(disease, user_country=None):
    """
    根据疾病+用户国家推荐医院，带fallback保护。
    """
    results = []

    try:
        for hospital in hospitals_data:
            # 如果能检测国家，优先按国家筛选
            if user_country:
                if hospital.get('country') == user_country:
                    for dis in hospital.get('supported_diseases', []):
                        if dis['en'] == disease:
                            results.append(hospital)
            else:
                # 如果国家检测失败，只按疾病匹配
                for dis in hospital.get('supported_diseases', []):
                    if dis['en'] == disease:
                        results.append(hospital)

            if len(results) >= 3:
                break

        # fallback兜底：如果找不到符合条件的医院，随便推荐3家
        if not results:
            print("🟠 fallback触发：无匹配医院，随机推荐3家")
            results = hospitals_data[:3]

    except Exception as e:
        print(f"❗️find_hospitals异常捕获: {e}")

    return [{
        "name_zh": h['name_zh'],
        "name_en": h['name_en'],
        "address_zh": h['address_zh'],
        "address_en": h['address_en'],
        "specialty_zh": h['specialty_zh'],
        "specialty_en": h['specialty_en'],
    } for h in results]