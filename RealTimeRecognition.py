import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import pyttsx3
#engine = pyttsx3.init()


# load saved model from PC
model = tf.keras.models.load_model('new_model_20ep3.h5')
model.summary()

# Define labels based on the dataset structure (25 classes: A-I, K-Y, Nothing)
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Nothing']
print(labels)

# Initialize text-to-speech engine once
engine = pyttsx3.init()

# Try multiple camera initialization strategies
camera_backends = [
    (cv2.CAP_DSHOW, "DirectShow"),
    (cv2.CAP_ANY, "Auto"),
    (cv2.CAP_MSMF, "Media Foundation"),
    (cv2.CAP_FFMPEG, "FFMPEG")
]

cap = None
working_backend = None

for backend_code, backend_name in camera_backends:
    print(f"Trying {backend_name} backend...")
    test_cap = cv2.VideoCapture(0, backend_code)
    
    if test_cap.isOpened():
        # Try to read a frame to verify it's working
        ret, frame = test_cap.read()
        if ret and frame is not None and frame.mean() > 10:  # Not black
            print(f"SUCCESS: {backend_name} backend working!")
            cap = test_cap
            working_backend = backend_name
            break
        else:
            print(f"Backend {backend_name} opened but frames are black/unreadable")
    else:
        print(f"Failed to open with {backend_name} backend")
    
    test_cap.release()

if cap is None:
    print("ERROR: No camera backend worked!")
    print("Please check:")
    print("1. Camera is connected and not used by another app")
    print("2. Camera drivers are properly installed")
    print("3. Try running Windows Camera app to verify camera works")
    exit()

print(f"Camera opened successfully with {working_backend} backend")
print(f"Camera resolution: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

# Set camera properties for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

while(True):
    
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5) 
    #region of intrest
    roi = frame[100:300, 100:300]
    img = cv2.resize(roi, (50, 50))
    cv2.imshow('roi', roi)
    

    img = img/255

    #make predication about the current frame
    prediction = model.predict(img.reshape(1,50,50,3))
    char_index = np.argmax(prediction)
    #print(char_index,prediction[0,char_index]*100)

    confidence = round(prediction[0,char_index]*100, 1)
    predicted_char = labels[char_index]

    # Use the pre-initialized engine
    engine.say(predicted_char) 
    engine.runAndWait()

    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    color = (0,255,255)
    thickness = 2

    #writing the predicted char and its confidence percentage to the frame
    msg = predicted_char +', Conf: ' +str(confidence)+' %'
    cv2.putText(frame, msg, (80, 80), font, fontScale, color, thickness)
    
    cv2.imshow('frame',frame)
    
    #close the camera when press 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
#release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
