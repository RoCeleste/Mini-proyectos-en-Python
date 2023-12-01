from PyQt6.QtWidgets import QWidget, QTextEdit, QLineEdit, QApplication, QPushButton, QGridLayout
import sys
import openai
import os
import threading

class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setWindowTitle("Chatbot")
        self.bot = Chatbot()

        layout = QGridLayout()
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.enviar_mensaje)

        self.enviar = QPushButton("Enviar")
        self.enviar.clicked.connect(self.enviar_mensaje)

        layout.addWidget(self.chat, 0, 0, 1, 3)
        layout.addWidget(self.input, 1, 0, 1, 3)
        layout.addWidget(self.enviar, 1, 3, 1, 4)

        self.setLayout(layout)

    def enviar_mensaje(self):
        input = self.input.text().strip()
        self.chat.append(f"<span style='color: #bb44ba'>YO:</span> {input}")
        self.input.clear()

        bot_thread = threading.Thread(target=self.respuesta_bot, args=[input])
        bot_thread.start()

    def respuesta_bot(self, input):
        respuesta = self.bot.respuesta(input)
        self.chat.append(f"<span style='color:#19d6e6'>BOT:</span> {respuesta}")


class Chatbot():

    def __init__(self):
        openai.api_key = "#Colocá aca tu API key de OpenAI. Andá a 'https://openai.com/product' y hace click en 'Get Started' para obtener una"

    def respuesta(self, input):
        res = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=input, max_tokens=2000, temperature=0.5).choices[0].text.strip()
        return res

app = QApplication(sys.argv)
home = Home()
home.show()
sys.exit(app.exec())
