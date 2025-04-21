# main.py
import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import Teniente  # tu módulo

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME") or "TRTT_bot"
WEBHOOK_PATH = f"/{BOT_USERNAME}"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

app = ApplicationBuilder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
scheduler = AsyncIOScheduler()

# ✅ Webhook: esta ruta será llamada por Telegram


@flask_app.route(WEBHOOK_PATH, methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), app.bot)
    # 👈 ejecutamos en background
    asyncio.create_task(app.process_update(update))
    return "ok", 200


async def setup():
    # 🔁 Comandos
    app.add_handler(CommandHandler("start", Teniente.start))
    app.add_handler(CommandHandler("recordar", Teniente.recordar))
    app.add_handler(CommandHandler("clima", Teniente.el_clima))
    app.add_handler(CommandHandler("frase", Teniente.frase))

    # 📅 Tareas
    scheduler.add_job(Teniente.nuevo_dia, trigger='cron',
                      hour=7, minute=0, args=[app.bot])
    scheduler.add_job(Teniente.enviar_nuevas_noticias,
                      trigger='interval', minutes=5, args=[app.bot])
    scheduler.add_job(Teniente.test_tarea, trigger='interval',
                      seconds=5, args=[app.bot])
    scheduler.start()

    await app.initialize()
    await app.start()
    await app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(setup())
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
