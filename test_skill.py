import json
from lambda_function import handler

def simulate_alexa_request(intent_name, query=None):
    """Simula una petición de Alexa"""
    
    # Estructura básica de una petición de Alexa
    request = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "test_session",
            "application": {
                "applicationId": "test_id"
            },
            "user": {
                "userId": "test_user"
            }
        },
        "context": {
            "System": {
                "application": {
                    "applicationId": "test_id"
                },
                "user": {
                    "userId": "test_user"
                }
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "test_request_id",
            "timestamp": "2024-03-17T12:00:00Z",
            "locale": "es-ES",
            "intent": {
                "name": intent_name,
                "slots": {}
            }
        }
    }
    
    # Añadir el slot de búsqueda si es necesario
    if query and intent_name == "BuscarInformacionIntent":
        request["request"]["intent"]["slots"] = {
            "query": {
                "name": "query",
                "value": query
            }
        }
    
    return request

def get_speech_text(response):
    """Extrae el texto de la respuesta de Alexa"""
    if 'response' in response and 'outputSpeech' in response['response']:
        output_speech = response['response']['outputSpeech']
        if 'ssml' in output_speech:
            # Eliminar las etiquetas SSML
            text = output_speech['ssml'].replace('<speak>', '').replace('</speak>', '')
            return text
        elif 'text' in output_speech:
            return output_speech['text']
    return "No se pudo obtener la respuesta"

def test_launch():
    """Prueba el inicio de la skill"""
    print("\n=== Probando LaunchRequest ===")
    request = simulate_alexa_request("LaunchRequest")
    request["request"]["type"] = "LaunchRequest"
    response = handler(request, None)
    print("Respuesta:", get_speech_text(response))

def test_buscar_informacion(query):
    """Prueba una búsqueda de información"""
    print(f"\n=== Probando búsqueda: '{query}' ===")
    request = simulate_alexa_request("BuscarInformacionIntent", query)
    response = handler(request, None)
    print("Respuesta:", get_speech_text(response))

def test_help():
    """Prueba la intención de ayuda"""
    print("\n=== Probando HelpIntent ===")
    request = simulate_alexa_request("AMAZON.HelpIntent")
    response = handler(request, None)
    print("Respuesta:", get_speech_text(response))

if __name__ == "__main__":
    print("Iniciando pruebas de la Skill Rey Salomón...")
    
    # Probar el inicio de la skill
    test_launch()
    
    # Probar algunas búsquedas
    test_buscar_informacion("qué es el universo")
    test_buscar_informacion("cuéntame sobre la historia de España")
    
    # Probar la ayuda
    test_help() 