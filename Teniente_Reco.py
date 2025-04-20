from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import Teniente
import os
from bot_functions import noticias


BOT_TOKEN = Teniente.BOT_TOKEN


async def main():
    global app
    app = ApplicationBuilder().token(BOT_TOKEN).build()

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

    # 🔁 Revisión de noticias cada 10 minutos
    scheduler.add_job(
        Teniente.enviar_nuevas_noticias,
        trigger='interval',
        minutes=10,
        args=[app.bot]
    )

    scheduler.start()

    os.system("cls")
    print("🤖 Bot en marcha...")
    # await app.initialize()
    # await app.start()
    await app.run_polling()


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
