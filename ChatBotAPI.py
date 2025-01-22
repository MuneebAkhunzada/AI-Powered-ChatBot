from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime
from openai import OpenAI
import openai

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
db = SQLAlchemy(app)
client = OpenAI('your-api-key')  

# Define a model for storing chat history
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(500))
    model_used = db.Column(db.String(100))
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

# Detect task type based on user query
def detect_task_type(query):
    query_lower = query.lower()
    if "code" in query_lower:
        return "gpt-4-turbo"
    elif "general" in query_lower:
        return "gpt-3.5-turbo"
    elif "reference" in query_lower:
        return "text-embedding-ada-002"
    else:
        return "gpt-3.5-turbo"

# Generate response based on detected model
def generate_response(query):
    try:
        model_id = detect_task_type(query)

        # For chat models (code, general)
        if model_id in ["gpt-4-turbo", "gpt-3.5-turbo"]:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing detailed explanations and suggestions."},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()

        # For 'reference' task, switch to GPT-3.5 Turbo for readable results
        elif model_id == "text-embedding-ada-002":
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable assistant. Provide clear and concise references for the given topic."},
                    {"role": "user", "content": f"Provide detailed references and resources for {query}."}
                ],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()

        # Log the conversation
        new_chat = ChatHistory(user_input=query, model_used=model_id, response=answer)
        db.session.add(new_chat)
        db.session.commit()

        return answer

    except Exception as e:
        return f"Error fetching response: {str(e)}"



# API route for continuous chat
@app.route('/chat', methods=['Post'])
def chat():
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("TalkBuddy: Goodbye! Have a great day!")
                break

            response = generate_response(user_input)
            print("\nTalkBuddy:", response)
            print("\n---------------------------------------------\n")
        return jsonify({"message": "Chat session ended."})

    except Exception as e:
        return jsonify({"error": str(e)})

# API route for chat history
@app.route('/history', methods=['GET'])
def get_history():
    history = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).all()
    chat_logs = [
        {
            "user_input": chat.user_input,
            "model_used": chat.model_used,
            "response": chat.response,
            "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for chat in history
    ]
    return jsonify(chat_logs)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
