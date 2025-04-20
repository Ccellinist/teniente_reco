import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WORDNIK_API_KEY")


def todays_word():
    url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={API_KEY}"
    response = requests.get(url)

    for i in range(5):
        if response.status_code == 200:
            data = response.json()
            palabra = data["word"].upper()
            definiciones = [d["text"] for d in data.get("definitions", [])]

            msg = "Today´s Word: " + palabra + "\n"
            msg += "MEANINGS:\n"
            for i in range(len(definiciones)):
                msg += str(i+1) + " - " + definiciones[i] + "\n"

            return msg
        else:
            print("Intentando de nuevo (Palabra del dia)")
