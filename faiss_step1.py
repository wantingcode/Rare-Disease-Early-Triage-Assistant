# faiss_step1.py

from faiss_search_module import FAISSSymptomSearcher

# 初始化检索器
searcher = FAISSSymptomSearcher(
    index_path="symptom_index_top20.faiss",
    mapping_path="symptom_mapping_top20.json"
)

def faiss_top3_search(user_input):
    """
    输入用户的一句话描述，返回Top3匹配症状。
    """
    top3_results = searcher.search(user_input, top_k=3)

    # 整理返回格式（可以后续直接挂到/chat用）
    formatted_results = []
    for res in top3_results:
        formatted_results.append({
            "matched_symptom": res['matched_symptom'],
            "disease_zh": res['disease_zh'],
            "disease_en": res['disease_en'],
            "level": res['level'],
            "lang": res['lang']
        })
    
    return formatted_results

# 单独测试
if __name__ == "__main__":
    user_message = "宝宝脸色发黄"
    matches = faiss_top3_search(user_message)
    for match in matches:
        print(match)