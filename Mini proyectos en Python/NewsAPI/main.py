import requests
import contacto

API_KEY = "#Ingresa tu token de NewsAPI acá, obtener una en 'https://newsapi.org/' haciendo click en 'Get API Key' y llenando el formulario."
URL = f"https://newsapi.org/v2/top-headlines?country=ar&apiKey={API_KEY}"
USERNAME = "#Ingresa el correo de origen de las noticias (usualmente el mismo que el correo de destino)"

req = requests.get(URL)
content = req.json()
print(content.keys())
body = ""
for article in content["articles"][:15]:            # Las primeras 15 noticias
    if article["title"] is not None:
        body = body + article["title"] + "\n" + article["url"] + 2*"\n"

body = body.encode("utf-8")
contacto.enviar_correo(USERNAME, body)
