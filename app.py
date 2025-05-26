from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(dotenv_path="superdash.env")

app = Flask(__name__)
CORS(app)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    # Serve the main dashboard HTML
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')

    # Create a ChatCompletion with OpenAI
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "Kamu adalah asisten ERP yang ramah dan responsif."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Maaf, terjadi kesalahan: {e}"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    # Get port from environment for Replit deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
