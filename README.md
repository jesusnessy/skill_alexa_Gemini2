# Skill de Alexa - Rey Salomón con Gemini 2.0

Esta skill de Alexa utiliza la inteligencia artificial de Google Gemini 2.0 para responder preguntas y buscar información a través de comandos de voz.

## Requisitos

- Cuenta de desarrollador de Amazon Alexa
- Cuenta de Google Cloud con acceso a la API de Gemini
- Python 3.7 o superior
- AWS Lambda

## Configuración

1. Clona este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz del proyecto con tu API key de Google:
   ```
   GOOGLE_API_KEY=tu_api_key_aquí
   ```

4. En la consola de desarrolladores de Alexa:
   - Crea una nueva skill
   - Sube el contenido de `skill.json` como manifiesto
   - Sube el contenido de `interactionModel.json` como modelo de interacción
   - Configura el endpoint de AWS Lambda con el código de `lambda_function.py`

## Uso

Para usar la skill:

1. Di "Alexa, abre Rey Salomón"
2. Haz tu pregunta, por ejemplo:
   - "Busca información sobre el universo"
   - "Qué sabes de la historia de Roma"
   - "Cuéntame sobre la inteligencia artificial"

## Características

- Integración con Gemini 2.0 para respuestas inteligentes
- Interfaz en español
- Manejo de errores robusto
- Respuestas naturales y contextuales

## Notas

- Asegúrate de tener una conexión a internet estable
- La API de Gemini tiene límites de uso, consulta la documentación de Google Cloud
- Las respuestas pueden variar según la complejidad de la pregunta 