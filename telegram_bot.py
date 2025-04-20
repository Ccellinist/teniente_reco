from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# Envia una notificacion a Telegram
async def mensaje(mensaje):
    bot = Bot(token=TOKEN)
    await enviar_mensaje(mensaje=mensaje, bot=bot, reintentos=5)


async def enviar_mensaje(mensaje, bot, reintentos=5):
    for i in range(reintentos):
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensaje)
            return True
        except:
            print("Algo faió Joven")
