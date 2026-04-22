# Database Setup Guide for Gesture Recognition System

## Prerequisites
- MySQL Server installed and running
- Python 3.8+

## Installation Steps

### 1. Install Required Dependencies
```bash
pip install -r requirements.txt
```

This will install the MySQL connector along with other dependencies.

### 2. Configure Database Connection
Edit `db_config.py` to match your MySQL credentials:

```python
def __init__(self):
    self.host = 'localhost'      # Your MySQL host
    self.port = 3306             # Your MySQL port
    self.user = 'root'           # Your MySQL username
    self.password = 'password'   # Your MySQL password
    self.database = 'gesture_recognition'  # Database name
```

### 3. Initialize the Database
Run the initialization script to create the database schema:

```bash
python init_db.py
```

This will:
- Create the `gesture_recognition` database
- Create the following tables:
  - `users` - Store user accounts
  - `gestures` - Store recognized gestures
  - `recognition_sessions` - Track recognition sessions
  - `gesture_statistics` - Store gesture recognition statistics
- Insert a default user (email: nagamjyothi691@gmail.com, password: sign@2026)

## Database Schema

### users table
- `id` - Primary key
- `email` - User email (unique)
- `password` - User password
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

### gestures table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `gesture_label` - Recognized gesture (A-Z, Nothing)
- `confidence` - Recognition confidence percentage
- `timestamp` - Recognition timestamp

### recognition_sessions table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `session_start` - Session start timestamp
- `session_end` - Session end timestamp
- `total_gestures` - Total gestures recognized in session

### gesture_statistics table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `gesture_label` - Gesture label
- `recognition_count` - Number of times recognized
- `last_recognized` - Last recognition timestamp

## Usage

### Automatic Gesture Storage
When you run the Flask app and use the real-time recognition feature, recognized gestures are automatically saved to the database when:
- Confidence is above 80%
- The gesture is stable for 3 consecutive frames
- The gesture is different from the last saved gesture OR 2 seconds have passed

### API Endpoints

#### Get Gesture History
```
GET /api/gesture_history?limit=50
```
Returns the last N recognized gestures for the logged-in user.

#### Get Gesture Statistics
```
GET /api/gesture_statistics
```
Returns recognition statistics for each gesture (count, last recognized time).

## Troubleshooting

### Connection Errors
If you get connection errors:
1. Verify MySQL Server is running
2. Check your credentials in `db_config.py`
3. Ensure the user has necessary privileges

### Database Not Created
If the database isn't created:
1. Run `python init_db.py` again
2. Check MySQL error logs
3. Verify your MySQL user has CREATE DATABASE privileges

## Security Notes
- Change the default password in `db_config.py` before production use
- Consider using environment variables for sensitive credentials
- Implement proper password hashing for user authentication
