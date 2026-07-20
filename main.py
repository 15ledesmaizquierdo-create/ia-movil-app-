from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

datos = [
    ("Hola", "saludo"), ("Buenos días", "saludo"), ("Hey", "saludo"), ("¿Qué tal?", "saludo"),
    ("Adiós", "despedida"), ("Nos vemos", "despedida"), ("Chao", "despedida"), ("Hasta luego", "despedida"),
    ("¿Quién eres?", "identidad"), ("¿Cómo te llamas?", "identidad"), ("¿Qué eres tú?", "identidad"),
    ("Gracias", "agradecimiento"), ("Muchas gracias", "agradecimiento"), ("Te agradezco", "agradecimiento"),
    ("Ayuda", "ayuda"), ("¿Qué sabes hacer?", "ayuda"), ("Necesito asistencia", "ayuda")
]

textos = [item[0] for item in datos]
etiquetas = [item[1] for item in datos]

vectorizador = CountVectorizer()
X_train = vectorizador.fit_transform(textos)
modelo = MultinomialNB()
modelo.fit(X_train, etiquetas)

respuestas = {
    "saludo": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "despedida": "¡Adiós! Que tengas un excelente día.",
    "identidad": "Soy tu inteligencia artificial móvil básica creada en Python.",
    "agradecimiento": "¡De nada! Estoy aquí para ayudarte.",
    "ayuda": "Puedo responder saludos, despedidas, preguntas sobre quién soy y agradecimientos."
}

def obtener_respuesta(mensaje):
    X_test = vectorizador.transform([mensaje])
    prediccion = modelo.predict(X_test)[0]
    probabilidad = np.max(modelo.predict_proba(X_test))

    if probabilidad < 0.15:
        return "No entiendo muy bien eso. ¿Podrías decirlo de otra forma?"
    return respuestas.get(prediccion, "Entendido.")

class IABasicaApp(App):
    def build(self):
        self.title = "IA Básica"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.chat_history = Label(
            text="IA: ¡Hola! Escribe un mensaje abajo.\n",
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('texture_size'))

        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(self.chat_history)
        layout.add_widget(scroll)

        self.user_input = TextInput(
            hint_text='Escribe algo...',
            size_hint=(1, 0.1),
            multiline=False
        )
        self.user_input.bind(on_text_validate=self.enviar_mensaje)
        layout.add_widget(self.user_input)

        btn = Button(text='Enviar', size_hint=(1, 0.1))
        btn.bind(on_press=self.enviar_mensaje)
        layout.add_widget(btn)

        return layout

    def enviar_mensaje(self, instance):
        texto = self.user_input.text.strip()
        if not texto:
            return

        self.chat_history.text += f"\nTú: {texto}"
        respuesta_ia = obtener_respuesta(texto)
        self.chat_history.text += f"\nIA: {respuesta_ia}\n"
        self.user_input.text = ""

if __name__ == '__main__':
    IABasicaApp().run()
