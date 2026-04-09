from apscheduler.schedulers.asyncio import AsyncIOScheduler
from stocks import get_stock_price
from bot import WATCHLIST
from telegram import Bot
import os

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
scheduler = AsyncIOScheduler()

async def check_prices():
    for user, stocks in WATCHLIST.items():
        for s in stocks:
            price = get_stock_price(s)
            if price > 200:
                await bot.send_message(user, f"🚨 {s} above $200 → ${price}")

scheduler.add_job(check_prices, "interval", minutes=60)
scheduler.start()
