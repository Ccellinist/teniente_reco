from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os
from dotenv import load_dotenv
from flask import Flask, request
import telegram

import telegram_bot
from bot_functions import noticias, clima, palabra_del_dia as pdd, cita
import tlg_msgs

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
# tu usuario de bot sin @, ej: TenienteRecoBot
BOT_USERNAME = os.getenv("BOT_USERNAME")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_USERNAME}"


app = Flask(__name__)
bot = telegram.Bot(token=BOT_TOKEN)


@app.route(f"/{BOT_USERNAME}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    app.update_queue.put_nowait(update)
    return "OK", 200


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(tlg_msgs.saludo_inicial)


async def recordar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        segundos = int(context.args[0])
        mensaje = " ".join(context.args[1:])
        await update.message.reply_text(f"⏳")
        await asyncio.sleep(segundos)
        await update.message.reply_text(f"🔔 Recordatorio: {mensaje}")
    except:
        await update.message.reply_text("No sabes ni crear un recordatorio?\nEs así!:\n/recordar [segundos] [mensaje]")


async def frase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.mensaje(cita.obtener_frase())


async def el_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.mensaje(clima.obtener_clima())


async def nuevo_dia(context: ContextTypes.DEFAULT_TYPE = None):
    print("¡Buenos días!")

    # for noticia in noticias.obtener_noticias():
    #     await telegram_bot.mensaje(noticia)
    await telegram_bot.mensaje(clima.obtener_clima())
    await telegram_bot.mensaje(pdd.todays_word())
    await telegram_bot.mensaje(cita.obtener_frase())


async def enviar_nuevas_noticias(context: ContextTypes.DEFAULT_TYPE = None):
    print("Revisión de noticias iniciada...")
    nuevas = noticias.obtener_nuevas_noticias()
    if nuevas:
        for noticia in nuevas:
            await telegram_bot.mensaje(noticia)
    else:
        await telegram_bot.mensaje("Sin nuevas noticias")
