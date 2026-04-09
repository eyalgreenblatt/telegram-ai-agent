import yfinance as yf

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    price = data["Close"].iloc[-1]
    return round(price, 2)
