import json
import pyttsx3
from capstone_gesture_control import *
from capstone_gesture_control.capstone_hand_ges import handgesture
from face_triplet.recognize_video import *

'''
    facerecog()
        input : 
        output : name , confidence

    handgesture()
        input : 
        output : list
'''
password = [0,1,2,3,4,5]
text_speech = pyttsx3.init()

def start():
    # Get User_Register Dictionary
    # file = open("./users_register.json","r")
    # data = json.load(file)

    # Face Module
    name,category=facerecog()
    print(name,category)

    # Categorization Logic
    if category.lower()=='master':
        text_speech.say("Please enter passcode")
        text_speech.runAndWait()
        # Matching password
        attempts = 1
        match = False
        while attempts<=3:
            # Hand Gesture Code Run - return sequence

            ans = handgesture()
            # Match Password
            match = ans == password
            ## 
            if match:
                # Latch Activate
                print("Access Granted.")
                break
            else:
                print("Wrong password. Try again")
                attempts+=1

        
        print("User Name : ",name)
    elif category.lower()=='known':
        # Text to Speech Code Run
        print("User Name : ",name)
        text_speech.say(name)
        text_speech.runAndWait()
    else:
        # Text to Speech Code Run "Unknown"
        print("Unknown User")

start()
