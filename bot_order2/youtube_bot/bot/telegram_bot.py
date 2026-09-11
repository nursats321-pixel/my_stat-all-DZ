import os
import asyncio
import yt_dlp

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


MAX_FILE_SIZE = 500 * 1024 * 1024


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Отправь ссылку на YouTube, "
        "и я скачаю видео."
    )


def download_video(url):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": (
            "bestvideo[height<=720]+bestaudio/"
            "best[height<=720]/"
            "best"
        ),

        "outtmpl": "downloads/%(title)s.%(ext)s",

        "noplaylist": True,

    
        "remote_components": "ejs:github",


        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    
    if not os.path.exists(filename):
        base_name = os.path.splitext(filename)[0]
        mp4_filename = base_name + ".mp4"

        if os.path.exists(mp4_filename):
            filename = mp4_filename

    return filename


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    url = update.message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text(
            "❌ Это не ссылка на YouTube."
        )
        return

    message = await update.message.reply_text(
        "⏳ Скачиваю видео..."
    )

    filename = None

    try:
        filename = await asyncio.to_thread(
            download_video,
            url
        )

        if not os.path.exists(filename):
            raise FileNotFoundError(
                "Скачанный файл не найден."
            )

        file_size = os.path.getsize(filename)
        size_mb = file_size / 1024 / 1024

        print(
            f"Видео скачано. Размер: {size_mb:.2f} МБ"
        )

        if file_size > MAX_FILE_SIZE:
            os.remove(filename)
            filename = None

            await message.edit_text(
                "❌ Видео слишком большое.\n\n"
                f"Размер: {size_mb:.1f} МБ\n"
                "Максимум: 500 МБ."
            )

            return

        await message.edit_text(
            f"📤 Отправляю видео...\n"
            f"Размер: {size_mb:.1f} МБ"
        )

        with open(filename, "rb") as video:
            await update.message.reply_document(
                document=video,
                filename=os.path.basename(filename)
            )

        os.remove(filename)
        filename = None

    except Exception as e:
        print(f"Ошибка: {e}")

        if filename and os.path.exists(filename):
            os.remove(filename)

        await message.edit_text(
            f"❌ Ошибка:\n\n{e}"
        )


async def main():

    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN не найден в .env"
        )

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("🤖 Telegram бот запущен...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()

    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())


