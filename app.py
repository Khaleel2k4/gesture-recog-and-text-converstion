from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import os
from db_config import db_config
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'signspeak_ai_secret_key_2024'

# Load the sign language recognition model
model = tf.keras.models.load_model('new_model_20ep3.h5')
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Nothing']

# Simple user database (in production, use a proper database)
users = {
    'nagamjyothi691@gmail.com': 'sign@2026'
}

# Database helper functions
def get_user_id(email):
    """Get user ID from database by email"""
    try:
        connection = db_config.get_connection()
        if not connection:
            return None
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0] if result else None
    except Error as e:
        print(f"Error getting user ID: {e}")
        return None

def save_gesture(user_id, gesture_label, confidence):
    """Save recognized gesture to database"""
    try:
        connection = db_config.get_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO gestures (user_id, gesture_label, confidence) VALUES (%s, %s, %s)",
            (user_id, gesture_label, confidence)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error saving gesture: {e}")
        return False

def get_gesture_history(user_id, limit=50):
    """Get gesture history for a user"""
    try:
        connection = db_config.get_connection()
        if not connection:
            return []
        cursor = connection.cursor()
        cursor.execute(
            "SELECT gesture_label, confidence, timestamp FROM gestures WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
            (user_id, limit)
        )
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [{'gesture': row[0], 'confidence': row[1], 'timestamp': row[2]} for row in results]
    except Error as e:
        print(f"Error getting gesture history: {e}")
        return []

def get_gesture_statistics(user_id):
    """Get gesture recognition statistics for a user"""
    try:
        connection = db_config.get_connection()
        if not connection:
            return []
        cursor = connection.cursor()
        cursor.execute(
            "SELECT gesture_label, recognition_count, last_recognized FROM gesture_statistics WHERE user_id = %s ORDER BY recognition_count DESC",
            (user_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [{'gesture': row[0], 'count': row[1], 'last_recognized': row[2]} for row in results]
    except Error as e:
        print(f"Error getting gesture statistics: {e}")
        return []

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
    
    user_id = get_user_id(session['username'])
    if not user_id:
        return redirect(url_for('login'))
    
    # Fetch gesture history and statistics
    gesture_history = get_gesture_history(user_id, limit=20)
    gesture_stats = get_gesture_statistics(user_id)
    
    # Calculate metrics
    total_detections = len(gesture_history)
    if total_detections > 0:
        avg_confidence = sum(g['confidence'] for g in gesture_history) / total_detections
        accuracy_rate = sum(1 for g in gesture_history if g['confidence'] >= 80) / total_detections * 100
        
        # Get last detected gesture time
        last_gesture = gesture_history[0]
        last_detected = last_gesture['timestamp']
    else:
        avg_confidence = 0
        accuracy_rate = 0
        last_detected = None
    
    return render_template('dashboard.html', 
                         gesture_history=gesture_history,
                         gesture_stats=gesture_stats,
                         total_detections=total_detections,
                         avg_confidence=round(avg_confidence, 1),
                         accuracy_rate=round(accuracy_rate, 1),
                         last_detected=last_detected)

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
    
    user_id = get_user_id(session['username'])
    if not user_id:
        return redirect(url_for('login'))
    
    # Fetch gesture history from database
    gesture_history = get_gesture_history(user_id, limit=1000)
    
    return render_template('history.html', gesture_history=gesture_history)

@app.route('/analytics')
def analytics():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_id = get_user_id(session['username'])
    if not user_id:
        return redirect(url_for('login'))
    
    # Fetch gesture history and statistics
    gesture_history = get_gesture_history(user_id, limit=100)
    gesture_stats = get_gesture_statistics(user_id)
    
    # Calculate metrics
    total_detections = len(gesture_history)
    if total_detections > 0:
        avg_confidence = sum(g['confidence'] for g in gesture_history) / total_detections
        accuracy_rate = sum(1 for g in gesture_history if g['confidence'] >= 80) / total_detections * 100
    else:
        avg_confidence = 0
        accuracy_rate = 0
    
    return render_template('analytics.html', 
                         gesture_history=gesture_history,
                         gesture_stats=gesture_stats,
                         total_detections=total_detections,
                         avg_confidence=round(avg_confidence, 1),
                         accuracy_rate=round(accuracy_rate, 1))

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

# Global variables for video streaming
camera = None
current_prediction = "Nothing"
current_confidence = 0
last_saved_gesture = None
last_saved_time = 0
current_user_id = None

# Stability variables
last_stable_prediction = "Nothing"
prediction_count = 0
confidence_threshold = 0.5  # 50% confidence threshold (lowered for better recognition)
min_stable_frames = 2  # Need 2 consecutive high-confidence predictions (lowered for faster response)

def generate_frames():
    global camera, current_prediction, current_confidence, last_stable_prediction, prediction_count, last_saved_gesture, last_saved_time, current_user_id
    import time
    
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
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Process frame for sign language recognition
        try:
            # Extract optimized ROI for better gesture detection
            roi_x1, roi_y1 = 120, 90
            roi_x2, roi_y2 = 280, 250
            cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 3) 
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            img = cv2.resize(roi, (50, 50))
            
            # Preprocess exactly like original working code
            img = img / 255.0
            
            # Make prediction with correct input shape (1, 50, 50, 3)
            predictions = model.predict(img.reshape(1, 50, 50, 3))
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0]) * 100
            
            # Stability logic to prevent random predictions
            predicted_label = labels[predicted_class]
            
            if confidence >= confidence_threshold * 100:
                if predicted_label == last_stable_prediction:
                    prediction_count += 1
                else:
                    last_stable_prediction = predicted_label
                    prediction_count = 1
                
                # Only update if we have enough consecutive predictions
                if prediction_count >= min_stable_frames:
                    current_prediction = predicted_label
                    current_confidence = confidence
                    
                    # Save gesture to database (avoid duplicates within 2 seconds)
                    current_time = time.time()
                    if (current_prediction != "Nothing" and 
                        (last_saved_gesture != current_prediction or 
                         current_time - last_saved_time > 2)):
                        if current_user_id:
                            save_gesture(current_user_id, current_prediction, current_confidence)
                            last_saved_gesture = current_prediction
                            last_saved_time = current_time
            else:
                # Reset count if confidence is too low
                prediction_count = 0
            
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
    global current_user_id
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Set current user ID for use in generate_frames
    current_user_id = get_user_id(session['username'])
    
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

@app.route('/api/gesture_history')
def api_gesture_history():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = get_user_id(session['username'])
    if not user_id:
        return jsonify({'error': 'User not found'}), 404
    
    limit = request.args.get('limit', 50, type=int)
    history = get_gesture_history(user_id, limit)
    return jsonify(history)

@app.route('/api/gesture_statistics')
def api_gesture_statistics():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = get_user_id(session['username'])
    if not user_id:
        return jsonify({'error': 'User not found'}), 404
    
    stats = get_gesture_statistics(user_id)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
