import speech_recognition as sr
import pyttsx3
import requests
import json
import os

# Groq API key
api_key = "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"  # Replace with your actual Groq API key

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}




url = "https://api.groq.com/openai/v1/chat/completions"
  
#endpoint
model_name = "llama3-8b-8192"  



# Function to send the query to Groq API and get a response
def get_groq_response(user_input):
    payload = {
        "model": model_name,  # Use correct model name
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    # Sending POST request to Groq API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the response is successful
    if response.status_code == 200:
        response_data = response.json()
        # Assuming the response contains the 'text' field with the AI response
        return response_data.get('choices', [{}])[0].get('message', {}).get('content', "Sorry, I couldn't get a response.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to speak the text
def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    """Recognizes speech and responds with voice."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your voice...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        speak(f"You said: {text}")  # Reply with voice

        # Send the recognized speech to Groq and get the response
        groq_response = get_groq_response(text)
        print(f"AI Response: {groq_response}")
        speak(groq_response)  # Speak the AI's response

        return text
    except sr.UnknownValueError:
        error_message = "Sorry, I could not understand the audio."
        print(error_message)
        speak(error_message)  # Reply with voice
        return None
    except sr.RequestError:
        error_message = "Could not request results from Google Speech Recognition service."
        print(error_message)
        speak(error_message)  # Reply with voice
        return None

# Test the speech recognition with voice reply
recognize_speech()
