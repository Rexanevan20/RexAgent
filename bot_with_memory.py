import os
import sqlite3
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")
AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://api.deepseek.com/v1")
AI_MODEL = os.environ.get("AI_MODEL", "deepseek-chat")

ai_client = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)

DB_FILE = "chat_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        role TEXT,
        content TEXT,
        timestamp DATETIME
    )''')
    conn.commit()
    conn.close()

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, role, content, datetime.now()))
    conn.commit()
    conn.close()

def get_conversation_history(user_id, limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
              (user_id, limit))
    messages = c.fetchall()
    conn.close()
    return [{"role": msg[0], "content": msg[1]} for msg in reversed(messages)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! King Rex Ada Yang Bisa Aku Bantu ?")

async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text
    save_message(user_id, "user", user_message)
    
    try:
        history = get_conversation_history(user_id, limit=10)
        messages = [{"role": "system", "content": "Kamu adalah asisten yang membalas dalam Bahasa Indonesia, singkat dan jelas. Jangan gunakan markdown formatting. Balasan harus plain text aja."}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        
        response = ai_client.chat.completions.create(model=AI_MODEL, messages=messages)
        ai_response = response.choices[0].message.content
        save_message(user_id, "assistant", ai_response)
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Waduh, ada masalah pas manggil AI-nya. Coba lagi bentar ya.")

def main():
    if not BOT_TOKEN or not AI_API_KEY:
        raise ValueError("Missing BOT_TOKEN atau AI_API_KEY")
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_ai))
    logger.info("Bot with memory mulai jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
