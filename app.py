from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyAUmlvp8lgyPRd3QEK5Bn2BYJ2-uftjgV4")


model = genai.GenerativeModel('gemini-2.0-flash')

conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.json
    user_message = data.get('message', '')
    
    user_content = {'role': 'user', 'parts': [{'text': user_message}]}
    
    try:
        chat = model.start_chat(history=conversation_history)
        
        response = chat.send_message(user_message)
        
        bot_response = response.text
        
        conversation_history.extend([
            user_content,
            {'role': 'model', 'parts': [{'text': bot_response}]}
        ])
        
        return jsonify({
            'status': 'success',
            'response': bot_response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f'Ocorreu um erro: {str(e)}'
        })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'success', 'message': 'Conversa reiniciada'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)