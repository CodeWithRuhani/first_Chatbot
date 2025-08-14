# Chatbot Application

A simple chatbot application using FastAPI backend and Streamlit frontend, powered by Google's Gemini AI.

## Setup

1. **Environment Setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the project root with your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Running the Application


### Option 2: Manual startup

1. **Start the Backend** (in one terminal):
   ```bash
   python main.py
   ```
   The FastAPI backend will run on `http://localhost:8000`

2. **Start the Frontend** (in another terminal):
   ```bash
   streamlit run front.py
   ```
   The Streamlit frontend will run on `http://localhost:8501`

## API Endpoints

- `GET /` - Health check endpoint
- `POST /chat` - Chat endpoint that accepts JSON: `{"message": "your message"}`

## File Structure

- `main.py` - FastAPI backend server
- `front.py` - Streamlit frontend interface
- `llm.py` - Gemini AI integration module
- `requirements.txt` - Python dependencies
- `run_app.sh` - Startup script
- `.env` - Environment variables (create this file)

## Troubleshooting

1. **Backend Connection Error**: Make sure the FastAPI backend is running on `http://127.0.0.1:8000`
2. **API Key Error**: Ensure your `GOOGLE_API_KEY` is set correctly in the `.env` file
3. **CORS Issues**: The backend is configured to allow requests from common Streamlit ports

## Development

- The FastAPI backend includes auto-reload functionality when running directly
- Streamlit will auto-reload when you save changes to `front.py`
