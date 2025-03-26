import os
import json
import google.generativeai as genai
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No se encontró la API key de Google en las variables de entorno")

genai.configure(api_key=GOOGLE_API_KEY)

# Inicializar el modelo
try:
    model = genai.GenerativeModel('models/gemini-2.0-pro-exp')
except Exception as e:
    print(f"Error al inicializar Gemini: {str(e)}")
    raise

class BuscarInformacionHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BuscarInformacionIntent")(handler_input)

    def handle(self, handler_input):
        try:
            # Obtener la consulta del usuario
            slots = handler_input.request_envelope.request.intent.slots
            if not slots or "query" not in slots:
                return handler_input.response_builder.speak(
                    "No he entendido tu pregunta. ¿Podrías reformularla?"
                ).ask("¿Qué te gustaría saber?").response

            query = slots["query"].value
            if not query:
                return handler_input.response_builder.speak(
                    "No he captado tu pregunta. ¿Podrías repetirla?"
                ).ask("¿Qué te gustaría saber?").response

            # Generar respuesta con Gemini
            response = model.generate_content(
                f"Responde en español de manera concisa y clara: {query}"
            )
            
            if not response or not response.text:
                return handler_input.response_builder.speak(
                    "Lo siento, no pude generar una respuesta. ¿Podrías intentar con otra pregunta?"
                ).ask("¿Qué más te gustaría saber?").response

            speech_text = response.text.strip()
            
            # Limitar la longitud de la respuesta para Alexa
            if len(speech_text) > 800:
                speech_text = speech_text[:800] + "..."

        except Exception as e:
            print(f"Error al procesar la consulta: {str(e)}")
            speech_text = "Lo siento, ha ocurrido un error al procesar tu consulta. Por favor, intenta de nuevo."

        return handler_input.response_builder.speak(speech_text).ask("¿Hay algo más en lo que pueda ayudarte?").response

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "¡Hola! Soy gemini consultor, tu gemini consultor con Gemini. Puedo ayudarte a buscar información sobre cualquier tema. ¿Qué te gustaría saber?"
        return handler_input.response_builder.speak(speech_text).ask("¿Sobre qué tema te gustaría aprender?").response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Puedes preguntarme cualquier cosa y utilizaré Gemini para buscar la información. Por ejemplo, puedes decir 'busca información sobre el universo' o 'qué sabes de la historia de Roma'."
        return handler_input.response_builder.speak(speech_text).ask("¿Qué te gustaría saber?").response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speech_text = "¡Hasta luego! Que tengas un excelente día."
        return handler_input.response_builder.speak(speech_text).response

# Crear el skill builder y registrar los handlers
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BuscarInformacionHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())

# Crear el handler principal
handler = sb.lambda_handler() 