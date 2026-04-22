from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import os

app = Flask(__name__)
app.secret_key = 'signspeak_ai_secret_key_2024'

# Load the sign language recognition model
model = tf.keras.models.load_model('new_model_20ep3.h5')
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Nothing']

# Simple user database (in production, use a proper database)
users = {
    'nagamjyothi691@gmail.com': 'sign@2026'
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful! Welcome to SignSpeak AI.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/start_recognition')
def start_recognition():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # This would start the sign language recognition
    # For now, we'll return a simple page
    return render_template('recognition.html')

@app.route('/realtime')
def realtime():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('realtime.html')

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('history.html')

@app.route('/analytics')
def analytics():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('analytics.html')

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

# Global variables for video streaming
camera = None
current_prediction = "Nothing"
current_confidence = 0

def generate_frames():
    global camera, current_prediction, current_confidence
    
    if camera is None:
        # Initialize camera with multiple backend attempts
        backends = [cv2.CAP_DSHOW, cv2.CAP_FFMPEG, cv2.CAP_MSMF]
        for backend in backends:
            camera = cv2.VideoCapture(0, backend)
            if camera.isOpened():
                break
        
        if camera is None or not camera.isOpened():
            print("Error: Could not open camera")
            return
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Process frame for sign language recognition
        try:
            # Extract region of interest (ROI) like original code
            cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5) 
            roi = frame[100:300, 100:300]
            img = cv2.resize(roi, (50, 50))
            
            # Preprocess exactly like original working code
            img = img / 255.0
            
            # Make prediction with correct input shape (1, 50, 50, 3)
            predictions = model.predict(img.reshape(1, 50, 50, 3))
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0]) * 100
            
            # Update global variables
            current_prediction = labels[predicted_class]
            current_confidence = confidence
            
            # Add text overlay to frame
            cv2.putText(frame, f"{current_prediction}: {confidence:.1f}%", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            cv2.putText(frame, "Error in prediction", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    if 'username' not in session:
        return redirect(url_for('login'))
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recognition_results')
def recognition_results():
    if 'username' not in session:
        return redirect(url_for('login'))
    return jsonify({
        'gesture': current_prediction,
        'confidence': round(current_confidence, 1)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
