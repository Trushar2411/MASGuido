import cv2
import time
import os
import threading
from qibullet import SimulationManager, PepperVirtual
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Function to make Pepper speak using TTS
def speak(message, filename):
    tts = gTTS(message)
    tts.save(filename)
    audio = AudioSegment.from_mp3(filename)
    play(audio)
    os.remove(filename)  # Optionally remove the temporary file after playing

# Functions for Pepper robot greetings and interactions
def wave(pepper):
    for _ in range(2):
        pepper.setAngles("RShoulderPitch", -0.5, 0.5)
        pepper.setAngles("RShoulderRoll", -1.5620, 0.5)
        pepper.setAngles("RElbowRoll", 1.5620, 0.5)
        time.sleep(1.0)
        pepper.setAngles("RElbowRoll", -1.5620, 0.5)
        time.sleep(1.0)

def normal(pepper):
    pepper.goToPosture("StandInit", 0.6)
    time.sleep(1.0)

def head_nod(pepper):
    for _ in range(2):
        pepper.setAngles("HeadPitch", 0.5, 0.5)  # Nod down
        time.sleep(1.0)
        pepper.setAngles("HeadPitch", -0.5, 0.5)  # Nod up
        time.sleep(1.0)

# Function to open the HTML chat interface
def open_chat_html():
    # Open the HTML file in the default web browser
    webbrowser.open("chat.html")

# Function to speak asynchronously
def speak_async(message, filename):
    threading.Thread(target=speak, args=(message, filename)).start()
    

# Pepper robot interaction sequence
def pepper_interaction(pepper):
    # Pepper's initial greeting
    wave(pepper)
    speak("Hello M A S Students", "message.mp3")
    normal(pepper)
    speak("Glad to see you", "message1.mp3")
    head_nod(pepper)

    # Ask the user how they want to chat
    chat_choice = input("Do you want to chat in the audio or chatbox? (type 'audiochat' or 'chatbox'): ").strip().lower()
    use_chatbox = chat_choice == 'chatbox'

    if use_chatbox:
        # Open the HTML chat interface in a separate thread
        threading.Thread(target=open_chat_html).start()

    # Rasa interaction loop
    while True:
        if use_chatbox:
            user_input = input("You (Chatbox - type 'done' to switch): ")
            if user_input.lower() == 'done':
                speak("Switching to audio chat.", "switch.mp3")
                use_chatbox = False
                continue
        else:
            user_input = input("You: ")
            if user_input.lower() in ['chatbox', 'switch']:
                speak("Switching to chatbox.", "switch.mp3")
                open_chat_html()
                use_chatbox = True
                continue

        if user_input.lower() in ['bye', 'goodbye', 'stop']:
            speak("Goodbye!", "goodbye.mp3")
            head_nod(pepper)
            break

        rasa_response = get_rasa_response(user_input)
        if rasa_response:
            pepper_response = rasa_response[0].get("text", "Sorry, I didn't understand that.")
            print(f"Pepper: {pepper_response}")
            speak_async(pepper_response, "pepper_response.mp3")
            head_nod(pepper)


# Face-tracking function using laptop's webcam
def face_tracking_and_interaction(pepper):
    # Initialize face detection and webcam
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    interaction_started = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calculate the center of the face
            center_x = x + w / 2
            center_y = y + h / 2
            image_center_x = frame.shape[1] / 2
            image_center_y = frame.shape[0] / 2

            # Calculate yaw and pitch for head movement
            yaw = -(center_x - image_center_x) / image_center_x * 0.5
            pitch = (center_y - image_center_y) / image_center_y * 0.5

            # Move Pepper's head
            pepper.setAngles(["HeadYaw", "HeadPitch"], [float(yaw), float(pitch)], 0.2)


            # Check if the face is centered to start the interaction
            if abs(center_x - image_center_x) < w * 0.1 and abs(center_y - image_center_y) < h * 0.1:
                if not interaction_started:
                    print("Face centered, starting full interaction...")
                    interaction_started = True
                    pepper_interaction(pepper)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    simulation_manager = SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)

    # Start face tracking and interaction
    face_tracking_and_interaction(pepper)

    # Keep the simulation running until the user closes it
    input("Press Enter to stop the simulation...")
    simulation_manager.stopSimulation(client_id)

if __name__ == "__main__":
    main()

