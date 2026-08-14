import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ---- Setup logging biar kalau ada error keliatan di log Railway ----
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---- Ambil bot token dari Environment Variable (bukan ditulis langsung di kode, biar aman) ----
BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dipanggil waktu user pertama kali chat /start ke bot"""
    await update.message.reply_text(
        "Halo! Bot aku udah nyala 🚀\n\n"
        "Coba kirim pesan apa aja, nanti aku bales."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sementara: bot cuma balikin lagi pesan yang km kirim (echo)"""
    pesan_masuk = update.message.text
    await update.message.reply_text(f"Km bilang: {pesan_masuk}")


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN belum di-set! Tambahin di Railway > Variables."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Daftar handler: command /start, dan pesan teks biasa
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot mulai jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
