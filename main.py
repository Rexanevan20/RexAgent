import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ---- Setup logging biar kalau ada error keliatan di log Railway ----
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---- Ambil semua kunci rahasia dari Environment Variable (bukan ditulis langsung di kode) ----
BOT_TOKEN = os.environ.get("BOT_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")
AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://seekai.cc/v1")
AI_MODEL = os.environ.get("AI_MODEL", "deepseek-v4-flash")  # ganti sesuai nama model yg ada di dashboard seekai.cc km

# ---- Client buat manggil AI ----
ai_client = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dipanggil waktu user pertama kali chat /start ke bot"""
    await update.message.reply_text ("Halo! King Rex Ada Yang Bisa Aku Bantu ?\n\n")


async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot mikir pake AI buat balas pesan"""
    pesan_masuk = update.message.text
    try:
        response = ai_client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "Kamu adalah asisten yang membalas dalam Bahasa Indonesia, singkat dan jelas. Jangan gunakan markdown formatting seperti **, __, #, atau format apapun. Balasan harus plain text aja."} 
                {"role": "user", "content": pesan_masuk},
            ],
        )
        balasan = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error manggil AI: {e}")
        balasan = "Waduh, ada masalah pas manggil AI-nya. Coba lagi bentar ya."

    await update.message.reply_text(balasan)


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN belum di-set! Tambahin di Railway > Variables."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Daftar handler: command /start, dan pesan teks biasa
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_ai))

    logger.info("Bot mulai jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
