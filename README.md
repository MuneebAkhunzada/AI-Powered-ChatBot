AI-Powered Chatbot using GPT-3.5 Turbo & GPT-4
Overview
This project is an AI-powered chatbot that leverages the capabilities of GPT-3.5 Turbo and GPT-4 to provide intelligent, context-aware responses. The chatbot dynamically selects the appropriate AI model based on the user's input and stores chat history in an SQLite database for future reference.

Features
🚀 Dynamic Model Selection

GPT-4 Turbo for code-related queries.
GPT-3.5 Turbo for general queries.
Text-Embedding Ada-002 for reference-based tasks.
📊 Chat History Management

Stores user queries, responses, and timestamps using SQLite.
Retrieve past conversations with ease.
🔗 API Endpoints

/chat – Continuous chatbot interaction.
/history – Retrieve stored chat history.
🛠 Built with Flask

Lightweight, fast, and easy-to-deploy architecture.
Project Structure
graphql

📂 AI-Powered-ChatBot/
│-- 📄 ChatBotAPI.py       # Main Flask API with chat logic and database handling
│-- 📄 requirements.txt    # Dependencies required to run the project
│-- 📄 README.md           # Project documentation
│-- 📂 __pycache__/        # Cached Python files
│-- 📂 migrations/         # Database migration files (if needed)
Installation Instructions
Prerequisites
Make sure you have the following installed:

Python 3.8+
Flask
OpenAI Python package
SQLite (built-in with Python)

Step 1: Clone the Repository
git clone https://github.com/MuneebAkhunzada/AI-Powered-ChatBot.git
cd AI-Powered-ChatBot

Step 2: Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Set Up Environment Variables
Create a .env file in the root directory and add your OpenAI API key:

env

OPENAI_API_KEY=your-api-key-here

Step 5: Run the Application
python ChatBotAPI.py
The chatbot API will start running at http://localhost:5000.

Usage
1. Start Chatting
Send a POST request to the /chat endpoint to start a chat session:
curl -X POST http://localhost:5000/chat
Then enter your queries in the terminal. Type exit, quit, or bye to end the session.

2. Retrieve Chat History
Access stored conversations using the following GET request:
curl http://localhost:5000/history
Code Explanation
1. Dynamic Model Selection
The chatbot intelligently selects the AI model based on the user's query:

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
2. Generating AI Responses
The chatbot processes queries and generates responses based on the detected model:

response = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ],
    max_tokens=500,
    temperature=0.7
)
3. Storing Chat History
User queries and responses are stored in an SQLite database:

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(500))
    model_used = db.Column(db.String(100))
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
Future Enhancements
Add voice input/output support.
Implement a web-based chat interface.
Introduce multilingual capabilities.
Deploy using Docker for easier scalability.
Contributing
If you'd like to contribute, feel free to fork the repository and submit a pull request with your improvements.

License
This project is open-source and available under the MIT License.
