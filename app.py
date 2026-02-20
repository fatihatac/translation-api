from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)
CORS(app)

VALID_API_KEY = os.environ.get('API_KEY', 'my_local_secret_key')

@app.route('/translate', methods=['POST'])
def translate_text():
    client_api_key = request.headers.get('x-api-key')

    if client_api_key != VALID_API_KEY:
        error_response = {"error":"Unauthorized: Invalid or missing API Key"}
        return jsonify(error_response), 401

    request_data = request.get_json()

    if not request_data:
        error_response = {"error":"Invalid JSON format"}
        return jsonify(error_response), 400
    
    text_to_translate = request_data.get('text')
    source_language = request_data.get('source', 'auto')
    target_language = request_data.get('target', "tr")

    if not text_to_translate:
        error_response = {"error":"Text field is required"}
        return jsonify(error_response), 400
    
    try:
        translator_instance = GoogleTranslator(source=source_language, target=target_language)
        translation_result = translator_instance.translate(text_to_translate)

        success_response = {
            "original_text": text_to_translate,
            "translated_text": translation_result,
            "source_language": source_language,
            "target_language": target_language
        }
        return jsonify(success_response), 200
    except Exception as translation_error:
        error_response = {"error": str(translation_error)}
        return jsonify(error_response), 500
    

if __name__ == '__main__':
    server_port = 5000
    app.run(host='0.0.0.0', port=server_port)