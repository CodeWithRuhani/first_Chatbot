import google.generativeai as genai

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini LLM and returns the generated text.
    The API key configuration is expected to be done externally (e.g., in main.py).

    Args:
        prompt (str): The user's input message.

    Returns:
        str: The text response from the Gemini LLM.
    """
    try:
        # Initialize the GenerativeModel with the desired model (e.g., gemini-2.5-flash)
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Generate content based on the prompt
        response = model.generate_content(prompt)
        # Return the text part of the response
        return response.text
    except Exception as e:
        # Log any errors that occur during API interaction
        print(f"Error interacting with Gemini LLM: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."

if __name__ == '__main__':
    # This block is for testing llms.py in isolation.
    # In a real application, genai.configure() would be called in the main app.
    import os
    from dotenv import load_dotenv
    load_dotenv() # Load environment variables from .env file
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        print("Testing llms.py directly...")
        test_prompt = "Hello, what is your purpose?"
        response = get_gemini_response(test_prompt)
        print(f"Prompt: {test_prompt}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error during direct test of llms.py: {e}")

