from langdetect import detect

def guess_country(text):
    """
    简单的语言检测器，根据输入语言推测国家。
    中文（zh-cn/zh-tw） ➔ CN
    英文（en） ➔ US
    其他默认 CN
    """
    try:
        lang = detect(text)
        print(f"🧠 语言检测结果: {lang}")
        if lang.startswith('zh'):
            return 'CN'
        elif lang == 'en':
            return 'US'
        else:
            return 'CN'
    except:
        return 'CN'