from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from flask import Flask, request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os
import Teniente

BOT_TOKEN = Teniente.BOT_TOKEN
BOT_USERNAME = os.getenv("BOT_USERNAME")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_USERNAME}"

flask_app = Flask(__name__)


@flask_app.route(f"/{BOT_USERNAME}", methods=["POST"])
def webhook():
    if app:
        update = Update.de_json(request.get_json(force=True), app.bot)
        asyncio.run(app.process_update(update))
    return "OK", 200


app = None  # App de Telegram, se inicializa en setup()


async def setup():
    global app
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", Teniente.start))
    app.add_handler(CommandHandler("recordar", Teniente.recordar))
    app.add_handler(CommandHandler("clima", Teniente.el_clima))
    app.add_handler(CommandHandler("frase", Teniente.frase))

    # Tareas programadas
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        Teniente.nuevo_dia,
        trigger='cron',
        hour=7,
        minute=0,
        second=0,
        args=[app.bot]
    )
    scheduler.add_job(
        Teniente.enviar_nuevas_noticias,
        trigger='interval',
        minutes=5,
        args=[app.bot]
    )
    scheduler.start()

    # Inicialización y webhook
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(f"{WEBHOOK_URL}")


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(setup())
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
