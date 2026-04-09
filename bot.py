import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

from agent import agent_decide
from stocks import get_stock_price
from stocks_news import get_stock_news
from surf_tools import get_surf_forecast
from surf_graph import create_wave_graph
from voice_tools import transcribe_voice

load_dotenv()

WATCHLIST = {}

# -------------------- COMMANDS --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 AI Agent Ready!\n\n"
        "📈 /add AAPL\n"
        "💲 /price AAPL\n"
        "📰 /news Tesla\n\n"
        "🌊 Ask about surf!\n"
        "Example: surf habonim 7 days\n"
        "או שלח הודעה קולית בעברית 🎤"
    )

async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper()
    user = update.effective_user.id
    WATCHLIST.setdefault(user, []).append(symbol)
    await update.message.reply_text(f"Added {symbol} to watchlist 📈")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper()
    price = get_stock_price(symbol)
    await update.message.reply_text(f"{symbol} price: ${price}")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    company = " ".join(context.args)
    news = get_stock_news(company)
    await update.message.reply_text(news)

# -------------------- MAIN AI CHAT --------------------

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    user_id = update.effective_user.id
    watchlist = WATCHLIST.get(user_id, [])

    await update.message.reply_text("🤖 Thinking...")

    try:
        # 🌊 SURF SKILL
        if "surf" in user_text or "wave" in user_text or "גל" in user_text:
            beach = "habonim" if "habonim" in user_text or "הבונים" in user_text else "tel aviv"
            days = 7 if "7" in user_text else 1
            lang = "he" if "גל" in user_text else "en"

            report, hours = get_surf_forecast(beach, days, lang)

            # Always send text forecast
            await update.message.reply_text(report)

            # Only create graph if API returned data
            if hours:
                try:
                    graph = create_wave_graph(hours, beach)
                    with open(graph, "rb") as img:
                        await update.message.reply_photo(img)
                except Exception as e:
                    print("Graph error:", e)
                    await update.message.reply_text("⚠️ Graph unavailable (API issue)")
            else:
                await update.message.reply_text("⚠️ No hourly data for graph")

            return

        # 🤖 CLAUDE AGENT fallback
        decision = agent_decide(user_text, watchlist)
        await update.message.reply_text(decision)

    except Exception as e:
        import traceback
        traceback.print_exc()
        await update.message.reply_text(f"🚨 BOT ERROR:\n{str(e)}")


# -------------------- VOICE HANDLER --------------------

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🎤 מקשיב להודעה הקולית...")

        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive("voice.ogg")

        text = transcribe_voice("voice.ogg")
        print("User said:", text)

        beach = "habonim" if "הבונים" in text else "tel aviv"
        report, hours = get_surf_forecast(beach, 7, "he")
        await update.message.reply_text(report)

        if hours:
            try:
                graph = create_wave_graph(hours, beach)
                with open(graph, "rb") as img:
                    await update.message.reply_photo(img)
            except:
                await update.message.reply_text("⚠️ גרף לא זמין כרגע")
        else:
            await update.message.reply_text("⚠️ אין נתוני שעות לגרף")


    except Exception as e:
        await update.message.reply_text(f"Voice error: {e}")

# -------------------- MAIN --------------------

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_stock))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("news", news))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
