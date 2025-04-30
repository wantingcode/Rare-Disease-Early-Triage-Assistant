from flask import Flask, render_template, request, jsonify, session
from langdetect import detect
from flask_cors import CORS
import faiss
import json
import os
from sentence_transformers import SentenceTransformer
from faiss_search_disease import search_top3_diseases
from disease_mapper import map_symptoms_to_diseases
from diagnosis_engine import score_diseases, get_top_disease
from dynamic_question_manager import initialize_session, get_next_question, record_answer, is_session_finished
from flask import session
from hospital_recommender_new import find_hospitals
from language_detect import guess_country  # ✅ 在这里加上！
# together_predict 和 find_hospitals 也应该是模块函数，假设已经有

def guess_country(text):
    lang = detect(text)
    if lang == "zh":
        return "CN"
    else:
        return "US"

# 载入 rare_disease_symptom_top20.json，并转换为以疾病英文名为 key 的 dict
def load_symptom_knowledge(filepath="symptom_mapping_top50.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    knowledge_dict = {}
    for item in data:
        disease = item['disease_en']
        primary = item.get('primary', [])
        secondary = item.get('secondary', [])
        knowledge_dict[disease] = {
            "primary": primary,
            "secondary": secondary
        }

    return knowledge_dict

# 初始化
symptom_knowledge = load_symptom_knowledge()

print("\n===================================")
print("🟢 系统初始化完成：")
print("   - symptom_mapping_top50 加载完毕 ✅")
print("   - FAISS 索引已就绪 ✅")
print("   - 多轮状态机 ready ✅")
print("   - 医院推荐模块 fallback 启用 ✅")
print("===================================\n")

app = Flask(__name__, static_folder='static')
app.secret_key = 'xwtwxtchrpc'  # 🔥 你自己设置一个随机字符串
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')   # 这里返回前端页面

# ---------------------- 配置区域 ----------------------
openai.api_key = '06ae601cc339c03d5ac17994e91267b756560271b55dde40958b10661b510af5'
openai.base_url = 'https://api.together.xyz/v1'
MODEL_NAME = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

with open('rare_disease_symptom_top20.json', 'r', encoding='utf-8') as f:
    symptom_knowledge = json.load(f)

index = faiss.read_index('symptom_index_top20.faiss')
with open('symptom_mapping_top20.json', 'r', encoding='utf-8') as f:
    symptom_mapping = json.load(f)

# ---------------------- 核心逻辑 ----------------------

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        print("\n🟠 收到新的POST请求")
        # ✅ 使用缓存的输入
        user_input = request.json.get('message') or session.get('user_input_text', '')
        user_answer = request.json.get('answer')

        print(f"🟠 解析到用户输入: {user_input}, 用户回答: {user_answer}")

         # ✅ 如果是新自然语言输入，强制清理旧的 session 状态
        if request.json.get('message'):
            session.pop('session_state', None)

        if 'session_state' not in session:
            print("🟠 首次输入，初始化追问状态机")

            # ✅ 缓存首次输入的 user_input
            session['user_input_text'] = user_input
            candidates = search_top3_diseases(user_input)
            print(f"🟠 召回Top3疾病: {candidates}")

            session_state = initialize_session(candidates)
            session['session_state'] = session_state

            question = get_next_question(session_state)
            print(f"🟠 第一个追问问题: {question}")

            return jsonify({
                'question': question,
                'modules': [],
                'final_disease': None,
                'hospitals': []
            })

        else:
            print("🟠 已存在会话，处理用户回答")
            session_state = session['session_state']

            if user_answer:
                record_answer(session_state, user_answer)

            if is_session_finished(session_state):
                print("✅ 追问完成，打分计算Top1疾病")
                scored = score_diseases(session_state['candidates'], session_state['answered'])
                final_disease = get_top_disease(scored)
                print(f"✅ 诊断结果Top1: {final_disease}")

                # ✅ 使用缓存 user_input 推断国家
                user_country = guess_country(user_input)
                hospitals = find_hospitals(final_disease, user_country)

        
                print(f"✅ 推荐医院: {hospitals}")

                session.pop('session_state')

                return jsonify({
                    'question': None,
                    'modules': session_state['collected_positive'],
                    'final_disease': final_disease,
                    'hospitals': hospitals
                })

            else:
                question = get_next_question(session_state)
                session['session_state'] = session_state

                return jsonify({
                    'question': question,
                    'modules': session_state['collected_positive'],
                    'final_disease': None,
                    'hospitals': []
                })
    except Exception as e:
        print(f"❌ chat接口发生异常: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)









    
