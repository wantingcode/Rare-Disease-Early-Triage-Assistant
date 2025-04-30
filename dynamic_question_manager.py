# dynamic_question_manager.py

import random
from symptom_mapping_loader import load_symptom_knowledge

# 加载症状知识库
symptom_knowledge = load_symptom_knowledge()

def initialize_session(candidates):
    """
    初始化多轮追问状态机
    """
    all_symptoms = set()
    seen = set()

    print(f"🟠 初始化Top3疾病: {candidates}")

    for disease in candidates:
        symptom_info = symptom_knowledge.get(disease, {})
        print(f"  ➤ {disease} 症状信息: {symptom_info}") 
        primary = symptom_info.get("primary", [])
        secondary = symptom_info.get("secondary", [])
        for s in primary + secondary:
            norm = s.lower().strip()
            if norm not in seen:
                seen.add(norm)
                all_symptoms.add(s)

    print(f"初始化Top3疾病症状追问池: {all_symptoms}")

    MAX_QUESTIONS = 10
    pending = list(all_symptoms)
    random.shuffle(pending)  # ✅ 可选：打乱顺序防止用户感知重复结构

    print(f"🟠 汇总症状池（打乱前）: {all_symptoms}")
    print(f"🟠 限制追问条数为 {MAX_QUESTIONS}")
    
    session_state = {
        "candidates": candidates,      # Top3 疾病
        "pending_questions": pending[:MAX_QUESTIONS],  # ✅ 限制最多10条
        "answered": {},                # 已回答的症状 {"症状文本": "yes"/"no"}
        "collected_positive": [],       # yes的症状（用于前端模块区展示）
        "current_question": None,
        "question_idx": 0
    }
    return session_state

def get_next_question(session_state):
    """
    从pending_questions里拿出下一个问题
    """
    if session_state["pending_questions"]:
        symptom = session_state["pending_questions"].pop(0)
        session_state["current_question"] = symptom
        return f"是否出现：{symptom}？"
    else:
        session_state["current_question"] = None
        return None

def record_answer(session_state, answer):
    """
    记录用户回答（yes/no）
    """
    symptom = session_state["current_question"]
    if symptom:
        session_state["answered"][symptom] = answer
        if answer == "yes":
            session_state["collected_positive"].append(symptom)

def is_session_finished(session_state):
    """
    判断是否所有问题都问完
    """
    return not session_state["pending_questions"] and len(session_state["answered"]) > 0