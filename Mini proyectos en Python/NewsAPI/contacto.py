import smtplib
import ssl
import os

def enviar_correo(des, mensaje):
     host = "smtp.gmail.com"
     puerto = 465

     usuario = "#Ingresa el correo de origen de las noticias (usualmente el mismo correo de destino)"
     password = "#Activar la verificacion de dos pasos del correo y activar app password. Instrucciones detalladas: 'https://www.youtube.com/watch?v=J4CtP1MBtOE'"

     mensaje = str(mensaje) + "\n" + str(des)

     with smtplib.SMTP_SSL(host, puerto, context=ssl.create_default_context()) as server:
         server.login(usuario, password)
         server.sendmail(usuario, des, mensaje)
