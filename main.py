from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # So that different ports of files can also work toether.
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from llm import get_gemini_response
# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow requests from the Streamlit frontend
# In a production environment, replace "*" with the specific origin of your Streamlit app (e.g., "http://localhost:8501")
origins = [
    "http://localhost",
    "http://localhost:8501",  # Default Streamlit port
    "http://127.0.0.1:8501",
    "http://127.0.0.1:8000",
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the Gemini API key
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please create a .env file.")
genai.configure(api_key=gemini_api_key)

# Define a Pydantic model for the request body
class Message(BaseModel):
    message: str

@app.get("/")
async def read_root():
    """
    Root endpoint to confirm the FastAPI server is running.
    """
    return {"message": "FastAPI Chatbot backend is running!"}

@app.post("/chat")
async def chat_endpoint(msg: Message):
    """
    API endpoint to handle chat messages.
    Receives a message from the frontend, sends it to the LLM,
    and returns the LLM's response.
    """
    user_message = msg.message
    print(f"Received message from frontend: {user_message}")

    # Get response from the Gemini LLM using the function from llm.py
    response = get_gemini_response(user_message)

    print(f"Sending response to frontend: {response}")
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using uvicorn
    # The --reload flag enables auto-reloading on code changes (for development)
    uvicorn.run(app, host="0.0.0.0", port=8000)


# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Hii"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Hello! How can I help you today?
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""I'm ravi"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Hi Ravi, nice to meet you. Is there anything I can assist you with today?
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Whats my name """),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Based on our current interaction, your name is Ravi.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "_main_":
    generate()



