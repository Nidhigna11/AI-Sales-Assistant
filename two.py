import sounddevice as sd
import numpy as np
import speech_recognition as sr
import requests
import json
import pyttsx3

def record_audio(duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait() 
    return recording, fs

def recognize_speech():
    recording, fs = record_audio()
    recognizer = sr.Recognizer()

    # Convert the recording to Recognizer-compatible format
    audio_data = np.squeeze(recording).astype(np.float32)
    audio = sr.AudioData(audio_data.tobytes(), fs, 2)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results.")
        return None

# response from Groq API(function)
def get_groq_response(input_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        'Authorization': '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',  
        'Content-Type': 'application/json',
    }
    data = {
        "model": "llama3-8b-8192",  
        "messages": [{"role": "user", "content": input_text}],
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to speak the response
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main loop to run the assistant
def run_sales_assistant():
    while True:
        # Step 1: (Listen to user speech)
        user_input = recognize_speech()

        if user_input:
            if user_input.lower() == "exit":
                print("Exiting the assistant...")
                break

            # Step 2: (Get response from Groq model)
            assistant_response = get_groq_response(user_input)

            # Step 3:( Display and speak the assistant's response)
            print(f"Assistant: {assistant_response}")
            speak_text(assistant_response)

# Run the sales assistant
if __name__ == "_main_":
    run_sales_assistant()