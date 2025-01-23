import requests
import json
import gradio as gr

# API Configuration
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}

# System message for chatbot context
SYSTEM = """
Your a therapist and your Theraphist name is Ned and you are a compassionate and empathetic mental health therapist with expertise in cognitive-behavioral therapy and mindfulness practices. Your role is to provide a safe and supportive environment for users to share their thoughts and feelings. Listen actively, ask insightful questions, and offer personalized guidance and coping strategies based on the user's concerns. Avoid making medical diagnoses or prescribing medications, and always encourage users to seek professional help if they seem to need it. Keep your tone warm, understanding, and encouraging.
"""

# Initialize conversation history with the system message
conversation_history = [SYSTEM]


def generate_response(prompt):
    try:
        # Add user input to conversation history
        conversation_history.append(f"User: {prompt}")

        # Use only the last 5 exchanges to reduce prompt size
        recent_history = "\n".join(conversation_history[-5:])

        # Prepare the API request
        data = {
            "model": "llama3.2",
            "stream": False,
            "prompt": recent_history,
            "max_tokens": 50,  # Limit response length
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            actual_response = response_data.get("response", "No response received.")
            conversation_history.append(f"Therapist: {actual_response}")
            return actual_response
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            print(error_message)
            return "An error occurred while generating a response. Please try again later."

    except Exception as e:
        print("Exception:", e)
        return "An unexpected error occurred. Please check the console for details."


# Gradio interface
iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
    title="Mental Health Chatbot",
    description="A chatbot providing empathetic and supportive responses for mental health concerns."
)

iface.launch()
