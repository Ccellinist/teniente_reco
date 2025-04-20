# %%
import telegram_bot
import bot_functions.palabra_del_dia as word


# %%
for noticia in news.obtener_noticias():
    await telegram_bot.mensaje(noticia)

# %%
for noticia in news.obtener_noticias():
    print(noticia)
# %%
