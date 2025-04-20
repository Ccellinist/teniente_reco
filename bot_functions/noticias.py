import feedparser
import json
import os

ARCHIVO_ENLACES = "enlaces_enviados.json"

# Cargar enlaces desde archivo JSON


def cargar_enlaces():
    if os.path.exists(ARCHIVO_ENLACES):
        with open(ARCHIVO_ENLACES, "r") as f:
            return set(json.load(f))
    return set()

# Guardar enlaces al archivo JSON


def guardar_enlaces(enlaces):
    with open(ARCHIVO_ENLACES, "w") as f:
        json.dump(list(enlaces), f)


# Inicializar
enlaces_enviados = cargar_enlaces()


# Sitios con API
# sites = ["http://feeds.bbci.co.uk/news/rss.xml",
#          "https://mexiconewsdaily.com/feed",
#          "https://www.excelsior.com.mx/rss.xml",
#          "https://www.reforma.com/rss/portada.xml",
#          "http://feeds.bbci.co.uk/news/world/rss.xml",
#          "https://globalnews.ca/feed/",
#          "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
#          "https://www.elfinanciero.com.mx/rss"
#          ]


def obtener_nuevas_noticias():
    RSS_URL = "https://www.elfinanciero.com.mx/rss"
    feed = feedparser.parse(RSS_URL)
    nuevas_noticias = []

    for entry in feed.entries:
        link = entry.link

        if link not in enlaces_enviados:
            enlaces_enviados.add(link)
            noticia = ""
            noticia += "📅 " + entry.get("published", "Fecha no disponible")
            noticia += "\n"
            noticia += "🔗 " + link
            noticia += "\n"
            nuevas_noticias.append(noticia)

    if nuevas_noticias:
        guardar_enlaces(enlaces_enviados)

    return nuevas_noticias
