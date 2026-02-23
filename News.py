import requests
import os

# 从环境变量中读取密钥（安全第一）
NEWS_CONF = os.getenv('NEWS_API_KEY')
AI_CONF = os.getenv('AI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_CHAT_ID')

def get_news():
    # 获取全球热门新闻
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_CONF}"
    response = requests.get(url).json()
    articles = response.get('articles', [])[:5] # 只取前5条
    return "\n".join([f"- {a['title']}: {a['description']}" for a in articles])

def get_ai_commentary(news_text):
    # 这里以调用 API 为例（伪代码，根据你用的 AI 调整）
    prompt = f"你是一个资深新闻评论员，请总结以下新闻并给出独到见解：\n{news_text}"
    # 调用 OpenAI/Gemini 的逻辑...
    return "这是 AI 生成的深度评论内容..."

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    raw_news = get_news()
    final_report = get_ai_commentary(raw_news)
    send_to_tg(final_report)