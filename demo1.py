import feedparser
import requests
import os
import google.generativeai as genai

# 配置 Gemini
genai.configure(api_key=os.getenv("AI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. 定义抓取函数
def get_top_news():
    feeds = [
        ("TechCrunch", "https://techcrunch.com/feed/"),
        ("The Verge", "https://www.theverge.com/rss/index.xml")
    ]
    
    collected_news = []
    for source_name, url in feeds:
        feed = feedparser.parse(url)
        # 每个源取前 3 条最新的
        for entry in feed.entries[:3]:
            # 使用 Jina Reader 获取网页净化的正文，以便 AI 深度阅读
            clean_content_url = f"https://r.jina.ai/{entry.link}"
            try:
                # 这一步是为了获取更完整的内容，如果嫌慢可以只传 entry.summary
                content_resp = requests.get(clean_content_url, timeout=10).text[:2000] # 截取前2000字
            except:
                content_resp = entry.summary

            collected_news.append({
                "source": source_name,
                "title": entry.title,
                "content": content_resp,
                "link": entry.link
            })
    return collected_news

# 2. 调用 Gemini 生成深度简报
def generate_report(news_list):
    prompt = f"""
    你是一个科技趋势观察家和资深评论员。以下是来自 TechCrunch 和 The Verge 的最新资讯：
    {news_list}
    
    请根据这些信息，撰写一份中文 Markdown 格式的早报。
    要求：
    1. 标题：# 🚀 科技前哨站 | 全球视野深度简报
    2. 对每条新闻进行【深度解析】：不要只重复事实，要结合行业趋势分析它的影响。
    3. 风格：犀利、理性、有前瞻性。
    4. 结尾：给出一个“今日趋势金句”。
    5. 使用标准的 Markdown 格式（分级标题、列表、引用块）。
    """
    
    response = model.generate_content(prompt)
    return response.text

# 3. 推送函数 (以 Webhook 为例)
def push_message(content):
    webhook_url = os.getenv("PUSH_URL")
    # 这里根据你的推送平台（钉钉/飞书/TG）调整 Payload 结构
    data = {
        "msgtype": "markdown",
        "markdown": {"title": "每日科技深评", "text": content}
    }
    requests.post(webhook_url, json=data)

if __name__ == "__main__":
    news_data = get_top_news()
    final_report = generate_report(news_data)
    push_message(final_report)
    print("推送完成！")