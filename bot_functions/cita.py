import requests


def obtener_frase():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    for i in range(5):
        if response.status_code == 200:
            data = response.json()
            frase = data[0]['q']
            autor = data[0]['a']
            return f"{frase}\n- {autor}"
        else:
            print("Reintentando Frase")
    return "Parece que hoy no habrá Frase bonita"
