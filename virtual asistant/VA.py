"""
Module: VA.py
Description: Automated voice assistant ('Honey') featuring speech recognition,
             localized command routing, and asynchronous text-to-speech rendering
             integrated with the Groq Cloud infrastructure.
"""

import os
import asyncio
import time
import speech_recognition as sr
import webbrowser
import sounddevice as sd
import numpy as np
import edge_tts
import ML
from playsound import playsound
from groq import Groq
from dotenv import load_dotenv

# --- CONFIGURATION & INITIALIZATION ---
# Load environment variables securely from local .env configuration
load_dotenv()
GROQ_API_KEY = os.getenv("gsk_jiuoQAziMERaHUQAiIdZWGdyb3FYq0sY9DoocLh8LuUUEyl") # API is deactived

# Instantiate enterprise API endpoints and peripheral listener tools
client = Groq(api_key=GROQ_API_KEY)
r = sr.Recognizer()


def speak(text: str) -> None:
    """
    Converts string input into an audio stream using edge-tts, 
    executes playback out loud, and handles runtime cleanup.
    """
    print(f"Honey: {text}")
    try:
        filename = "temp_voice.mp3"
        
        # Configure natural speech parameters (AvaNeural framework at accelerated speed)
        communicate = edge_tts.Communicate(text, "en-US-AvaNeural", rate="+10%")
        asyncio.run(communicate.save(filename))
        
        # Execute localized audio playback and purge temporary assets
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Speech Engine Error: {e}")


def ask_ai_brain(user_message: str) -> str:
    """
    Transfers unrouted runtime commands to the cloud-hosted 
    Llama infrastructure for dynamic NLP inference.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "You are Honey, a helpful, polite, and witty AI voice assistant. Keep your answers brief, friendly, and direct so they sound natural when spoken out loud."
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I had trouble connecting to my brain. Error: {e}"


# --- RUNTIME EXECUTION LOOP ---

if __name__ == "__main__":
    speak("How may I help you, sir?")
    print("Honey system initialized. Listening for wake word...")

    while True:
        try:
            print("\nListening for 'Hello'...")
            sample_rate = 16000
            duration = 1.5      
            
            # Record primary audio buffer for wake word detection
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()  
            
            # Format raw byte arrays to fulfill speech recognition prerequisites
            audio_data = sr.AudioData(recording.tobytes(), sample_rate, 2)
            query = r.recognize_google(audio_data, language="en-US").lower()
            print(f"User said: {query}")
            
            # --- INTERRUPT ARCHITECTURE & ROUTING ---
            if "hello" in query:
                speak("Yes sirr, awaiting command.")
                print("\nAwaiting command...")  
                
                # Capture extended command stream
                command_recording = sd.rec(int(5 * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
                sd.wait() 
                
                command_audio = sr.AudioData(command_recording.tobytes(), sample_rate, 2)
                command_query = r.recognize_google(command_audio, language="en-US").lower()
                print(f"Processing command: {command_query}")
                
                # --- STATIC COMMAND MATCHING ---
                if "open google" in command_query:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                    
                elif "youtube" in command_query:
                    speak("Opening Youtube")
                    webbrowser.open("https://www.youtube.com/")
                    
                elif "w a" in command_query: 
                    speak("Opening Whatsapp")
                    webbrowser.open("https://web.whatsapp.com/")
                    
                elif "typing" in command_query:
                    speak("Opening Typing Master")
                    webbrowser.open("https://www.edclub.com/sportal/program-3.game")
                    
                elif command_query.startswith("play "):
                    song = command_query.replace("play ", "").strip()
                    if song in ML.music:
                        link = ML.music[song]
                        speak(f"Playing {song}")
                        webbrowser.open(link)
                    else:
                        speak(f"Sorry, I couldn't find {song} in your music library.")    
                        
                elif "stop" in command_query or "exit" in command_query:
                    speak("Goodbye, sir.")
                    break 
                    
                # --- DYNAMIC AI OVERFLOW ---
                else:
                    print("Sending command to AI Brain...")
                    ai_response = ask_ai_brain(command_query)
                    speak(ai_response)
                
                print("Returning to standby mode.")
                time.sleep(0.5)

        except sr.UnknownValueError:
            # Handle silent runtime exceptions gracefully without killing the main thread
            pass
        except Exception as e:
            print(f"System Error: {e}")