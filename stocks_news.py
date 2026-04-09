import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def get_stock_news(company):
    articles = newsapi.get_everything(
        q=company,
        language="en",
        sort_by="publishedAt",
        page_size=3
    )

    news_list = []
    for a in articles["articles"]:
        news_list.append(f"📰 {a['title']}\n{a['url']}")
    return "\n\n".join(news_list)
