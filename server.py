from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    # Placeholder for real LLM integration
    # In a real app, you would call OpenAI or a local model here
    return jsonify({"response": f"Echo from server: {user_message}"})

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(port=5000, debug=True)