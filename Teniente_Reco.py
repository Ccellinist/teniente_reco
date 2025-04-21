from telegram.ext import ApplicationBuilder, CommandHandler, Application
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import Teniente
import os
from flask import Flask, request


BOT_TOKEN = Teniente.BOT_TOKEN
# tu usuario de bot sin @, ej: TenienteRecoBot
BOT_USERNAME = os.getenv("BOT_USERNAME")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_USERNAME}"


async def setup():
    os.system("cls")

    global app
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", Teniente.start))

    # Establecer webhook
    await app.bot.set_webhook(WEBHOOK_URL)
    await app.start()

    app.add_handler(CommandHandler("start", Teniente.start))
    app.add_handler(CommandHandler("recordar", Teniente.recordar))
    app.add_handler(CommandHandler("clima", Teniente.el_clima))
    app.add_handler(CommandHandler("frase", Teniente.frase))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        Teniente.nuevo_dia,
        trigger='cron',
        hour=7,
        minute=0,
        second=0,
        args=[app.bot]
    )

    # Revisión de noticias cada 10 minutos
    scheduler.add_job(
        Teniente.enviar_nuevas_noticias,
        trigger='interval',
        minutes=5,
        args=[app.bot]
    )

    scheduler.start()

    print("🤖 Bot en marcha...")
    # await app.initialize()
    # await app.start()
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
