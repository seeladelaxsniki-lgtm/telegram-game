import requests
import time

TOKEN = "8749530424:AAGizeCaRJl1ReRkI-1j8Lefy0neB0Wh8o4"
URL = f"https://api.telegram.org/bot{TOKEN}"

last_update = 0

while True:
    try:
        r = requests.get(URL + f"/getUpdates?offset={last_update+1}").json()

        for result in r.get("result", []):
            last_update = result["update_id"]

            chat_id = result["message"]["chat"]["id"]
            text = result["message"].get("text", "")

            if text == "/start":
                requests.get(URL + f"/sendMessage?chat_id={chat_id}&text=Bot is alive 24/7 🚀")

    except:
        pass

    time.sleep(2)