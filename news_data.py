import requests
from datetime import datetime, timedelta
from config import Config

def get_recent_news_titles(ticker: str, days: int = 30, limit: int = 5):
    """Devuelve una lista de títulos recientes (últimos `days` días) para el ticker usando NewsAPI."""
    since = (datetime.today() - timedelta(days=days)).date()
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={ticker}&from={since}&sortBy=popularity&apiKey={Config.NEWSAPI_API_KEY}"
    )
    r = requests.get(url)
    if r.status_code != 200:
        return []
    articles = r.json().get("articles", []) or []
    titles = [a.get("title", "") for a in articles if a.get("title")]
    return titles[:limit]
    

# titles = get_recent_news_titles("TSLA")
# print(titles)