from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os
from dotenv import load_dotenv

import telegram_bot
from bot_functions import noticias, clima, palabra_del_dia as pdd, cita
import tlg_msgs

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(tlg_msgs.saludo_inicial)


async def recordar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        segundos = int(context.args[0])
        mensaje = " ".join(context.args[1:])
        await update.message.reply_text(f"⏳ Te recordaré esto en {segundos} segundos: {mensaje}")
        await asyncio.sleep(segundos)
        await update.message.reply_text(f"🔔 Recordatorio: {mensaje}")
    except:
        await update.message.reply_text("Hasta para crear un recordatorio vales verga\nEs así:\n/recordar [segundos] [mensaje]")


async def frase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.mensaje(cita.obtener_frase())


async def el_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.mensaje(clima.obtener_clima())


async def nuevo_dia(context: ContextTypes.DEFAULT_TYPE = None):
    await telegram_bot.mensaje("🌞 ¡Buenos días!")

    # for noticia in noticias.obtener_noticias():
    #     await telegram_bot.mensaje(noticia)
    await telegram_bot.mensaje(clima.obtener_clima())
    await telegram_bot.mensaje(pdd.todays_word())
    await telegram_bot.mensaje(cita.obtener_frase())


async def enviar_nuevas_noticias():
    for noticia in noticias.obtener_nuevas_noticias():
        await telegram_bot.mensaje(noticia)
