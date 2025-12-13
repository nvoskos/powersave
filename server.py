from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Import and register Waste Fee API Blueprint
from waste_fee_api import waste_api
app.register_blueprint(waste_api)

# Import and register Notifications API Blueprint
from notifications_api import notifications_api
app.register_blueprint(notifications_api)

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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "PowerSave API",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    print("=" * 50)
    print("  PowerSave Server v1.0")
    print("  Waste Fee Offset System")
    print("=" * 50)
    print("\nEndpoints:")
    print("  - /api/municipalities")
    print("  - /api/properties/*")
    print("  - /api/wallet/*")
    print("  - /api/sessions/*")
    print("  - /api/payments/*")
    print("  - /api/notifications/*")
    print("  - /api/tips")
    print("  - /api/faq")
    print("\nStarting on http://localhost:5000")
    print("=" * 50)
    app.run(port=5000, debug=True)