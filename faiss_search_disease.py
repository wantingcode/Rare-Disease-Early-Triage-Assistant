# faiss_search_disease.py
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from langdetect import detect

# 加载模型（直接在这里）
cn_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
en_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 内置语言检测
def detect_language(text):
    lang = detect(text)
    if lang == "zh":
        return "zh"
    else:
        return "en"

# 内置编码
def encode_text(text):
    lang = detect_language(text)
    if lang == "zh":
        return cn_model.encode(text)
    else:
        return en_model.encode(text)

# 加载疾病描述数据
with open('disease_data_demo.json', 'r', encoding='utf-8') as f:
    disease_data = json.load(f)

# 分别提取中英文疾病列表
zh_disease_list = [item['disease_zh'] for item in disease_data]
en_disease_list = [item['disease_en'] for item in disease_data]

# 加载中英文FAISS索引
zh_index = faiss.read_index('disease_index_zh.faiss')
en_index = faiss.read_index('disease_index_en.faiss')

def search_top3_diseases(user_input):
    print(f"🧠 FAISS 检索中，用户输入: {user_input}")
    """
    输入用户自然语言 -> 返回 Top3 疾病列表
    """
    # 先编码
    embedding = encode_text(user_input)
    # 判断语言
    lang = detect_language(user_input)

    if lang == 'zh':
        D, I = zh_index.search(np.expand_dims(embedding, axis=0), 3)
        top3 = [zh_disease_list[idx] for idx in I[0]]
    else:
        D, I = en_index.search(np.expand_dims(embedding, axis=0), 3)
        top3 = [en_disease_list[idx] for idx in I[0]]

    print(f"🔍 FAISS Top3 症状: {top3}")  
    
    return top3