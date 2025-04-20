import feedparser


def obtener_noticias():
    RSS_URL = "https://www.elfinanciero.com.mx/rss"

    # Parsear el RSS
    feed = feedparser.parse(RSS_URL)

    noticias = []

    for entry in feed.entries:
        noticia = ""
        noticia += "📅" + entry.published if "published" in entry else "Fecha No disponible"
        noticia += "\n"
        noticia += "🔗" + entry.link
        noticia += "\n"
        noticias.append(noticia)

    return noticias
