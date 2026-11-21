# Context-Aware AI Chatbot

## Project Overview

The Context-Aware AI Chatbot is an intelligent conversational application powered by Google's Gemini API. It maintains conversation history and uses context window management to provide meaningful responses based on previous messages.

Unlike a basic chatbot that processes each message independently, this application maintains separate conversation histories using unique conversation IDs, allowing the chatbot to remember earlier interactions within a conversation.

## Features

- **Real LLM Integration:** Uses Google Gemini API to generate intelligent responses.
- **Multi-Turn Conversations:** Maintains conversation history for each conversation.
- **Context Window Management:** Uses a sliding-window strategy to send only the latest 10 messages to the LLM.
- **System Prompt:** Defines the chatbot as a friendly learning assistant.
- **Conversation Isolation:** Maintains separate histories using unique conversation IDs.
- **Error Handling:** Handles API failures, empty messages, and request timeouts.
- **Interactive Frontend:** Provides a simple interface using HTML, CSS, and JavaScript.
- **Environment Variable Security:** Stores the Gemini API key in an environment file.

## Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| LLM Provider | Google Gemini API |
| Python SDK | Google Gen AI SDK |
| Environment Management | python-dotenv |
| API Communication | REST API |

## Project Structure

```text
project_1_chatbot/
│
├── backend/
│   ├── main.py
│   ├── chatbot.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd project_1_chatbot
```

### 2. Create a Virtual Environment

```bash
cd backend
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API Key

Create a `.env` file inside the backend directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your actual Gemini API key.

Never upload your `.env` file to GitHub.

### 6. Start the Backend Server

From the backend directory, execute:

```bash
uvicorn main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 7. Run the Frontend

Open the `frontend/index.html` file using VS Code Live Server.

The frontend communicates with the FastAPI backend through the `/chat` endpoint.

## Context Management Strategy

The application uses a sliding-window context management strategy.

A maximum of 10 recent messages are retained and sent to the Gemini API for each response.

Example:

```python
MAX_MESSAGES = 10
context = updated_history[-MAX_MESSAGES:]
```

This prevents unlimited conversation history from being sent to the language model.

The system prompt is provided separately to maintain the chatbot's defined role and behaviour.

## Conversation History Management

Each conversation is assigned a unique conversation ID.

The backend uses this ID to retrieve and update the corresponding conversation history.

This ensures that separate conversations do not share their message history.

**Note:** Conversation histories are currently stored in an in-memory Python dictionary. They are cleared when the backend process restarts.

## API Endpoint

**POST** `/chat`

Request body:

```json
{
  "conversation_id": null,
  "message": "Hello, my name is Vidya"
}
```

Example response:

```json
{
  "conversation_id": "generated-conversation-id",
  "response": "Hello Vidya! Nice to meet you."
}
```

The generated conversation ID should be sent with subsequent messages to maintain the same conversation.

## Error Handling

The application handles:

- Empty user messages.
- Gemini API failures.
- API request timeouts.
- Empty AI responses.
- Backend service errors.

Clear error messages are returned to the frontend when requests fail.

## Future Enhancements

- Persistent conversation storage using a database.
- Conversation history retrieval after browser refresh.
- Support for multiple conversations.
- Improved responsive user interface.
- Conversation summarisation for longer discussions.

## Author

Developed as part of an internship project to demonstrate LLM integration, multi-turn conversation handling, and context window management.