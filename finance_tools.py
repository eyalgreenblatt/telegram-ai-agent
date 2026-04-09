import yfinance as yf
import requests

# Get stock price and stats
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    data = {
        "symbol": ticker,
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "name": info.get("longName")
    }
    return data


# Get latest news about stock
def get_stock_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey=YOUR_NEWSAPI_KEY"
    r = requests.get(url).json()
    
    articles = []
    for a in r.get("articles", [])[:5]:
        articles.append(f"{a['title']} - {a['source']['name']}")
    
    return articles
