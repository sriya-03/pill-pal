import openai
from flask import Flask, request, jsonify
import os  

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [{"role": "system", "content": "You are a pharmacist"}]

@app.route('/')
def home():
    return "ChatGPT Flask API"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        messages.append({"role": "user", "content": user_message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            if response:
                ChatGPT_reply = response["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": ChatGPT_reply})
                return jsonify({"reply": ChatGPT_reply})
            else:
                return jsonify({"error": "An error occurred during the API call."})
        except Exception as e:
            return jsonify({"error": f"An error occurred during the API call: {e}"})
    else:
        return jsonify({"error": "No message provided."})

if __name__ == "__main__":
    app.run(debug=True)