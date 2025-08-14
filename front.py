import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Chatbot", layout="centered", page_icon="🤖")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .status-indicator {
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .status-online {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🤖 AI Chatbot</h1>', unsafe_allow_html=True)

# Check backend status
def check_backend_status():
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

# Display backend status
backend_online = check_backend_status()
if backend_online:
    st.markdown('<div class="status-indicator status-online">✅ Backend Connected</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-indicator status-offline">❌ Backend Offline - Please start the FastAPI server</div>', unsafe_allow_html=True)
    st.info("Run `python main.py` in a separate terminal to start the backend server.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Type your message here...", disabled=not backend_online):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat", 
                    json={"message": user_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    reply = response.json().get("response", "No reply received")
                else:
                    reply = f"Server error: {response.status_code} - {response.text}"
                    
            except requests.exceptions.ConnectionError:
                reply = "❌ Cannot connect to the backend server. Please make sure it's running on http://127.0.0.1:8000"
            except requests.exceptions.Timeout:
                reply = "⏱️ Request timed out. The server might be busy."
            except Exception as e:
                reply = f"❌ Unexpected error: {str(e)}"
        
        st.markdown(reply)
    
    # Add bot response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# Sidebar with additional info
with st.sidebar:
    st.markdown("### About")
    st.info("This chatbot uses Google's Gemini AI to provide intelligent responses.")
    
    st.markdown("### Settings")
    if st.button("Clear Chat History"):
        st.session_state["messages"] = []
        st.rerun()
    
    st.markdown("### Status")
    st.write(f"Backend: {'🟢 Online' if backend_online else '🔴 Offline'}")
    st.write(f"Messages: {len(st.session_state['messages'])}")
    
    if st.button("Refresh Connection"):
        st.rerun()