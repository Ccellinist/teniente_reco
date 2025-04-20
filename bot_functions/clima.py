import requests
import tlg_msgs


def obtener_clima():
    CIUDAD = "Querétaro"
    url = f"https://wttr.in/{CIUDAD}?format=%C+%t+%w&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return tlg_msgs.sin_clima
