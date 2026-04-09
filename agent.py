import os
from anthropic import Anthropic
from finance_tools import get_stock_data, get_stock_news
from surf_tools import get_surf_forecast

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(prompt):
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text

    except Exception as e:
        return f"Claude error: {str(e)}"

def surf_report(user_text):

    beaches = ["tel aviv","herzliya","haifa","ashdod","ashkelon","netanya","habonim"]
    beach_found = "tel aviv"

    for b in beaches:
        if b in user_text.lower():
            beach_found = b

    surf = get_surf_forecast(beach_found)

    prompt = f"""
You are a professional surf instructor in Israel.

Surf data:
{surf}

Explain simply:
• Is it good for surfing?
• Skill level?
• Should I go surf?
• Give short recommendation.
"""

    return ask_claude(prompt)



def agent_decide(user_text, watchlist):
    ticker = user_text.upper().strip()

    text = user_text.lower()

    # 🌊 SURF SKILL  ← MUST BE INDENTED INSIDE FUNCTION
    if "surf" in text or "wave" in text or "sea" in text:
        
        days = 1
        beach = "tel aviv"

        if "7" in text or "week" in text:
            days = 7
        elif "3" in text:
            days = 3

        for b in ["tel aviv","herzliya","haifa","ashdod","netanya","habonim"]:
            if b in text:
                beach = b

        return get_surf_forecast(beach, days)


    # get finance data
    stock = get_stock_data(ticker)
    news = get_stock_news(ticker)

    prompt = f"""
You are a professional Wall Street stock analyst.

User asked about: {ticker}

Stock data:
{stock}

Latest News:
{news}

Give a short analysis:
• What the company does
• Is sentiment bullish or bearish?
• Key risks
• Short term outlook
"""

    answer = ask_claude(prompt)
    return answer
