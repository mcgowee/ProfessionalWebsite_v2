from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import process_message
from wordle_solver import process_wordle_request
import logging

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    filename="test_chatbot.log",  # Log file name
    level=logging.DEBUG,         # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://sakuraai.cloud", "https://www.sakuraai.cloud", "https://sakuraai.org", "https://www.sakuraai.org"]}})

SECRET_API_KEY = os.environ.get("FLASK_API_KEY", "")

def require_api_key():
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {SECRET_API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

# ---- Wordle Code (Unchanged) ---- #
@app.route("/solve", methods=["POST"])
def solve():
    """
    Wordle Solver endpoint: processes guesses and feedback to suggest words.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.json
    return process_wordle_request(data)

# ---- Chatbot Code ---- #

@app.route("/chat", methods=["POST"])
def chat():
    """
    Chatbot endpoint: accepts user input, processes it, and returns a response.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.json
    session_id = data.get("session_id")
    user_message = data.get("message", "")

    if not session_id:
        return jsonify({"error": "Session ID is required."}), 400

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Call the chatbot logic
    response_message = process_message(user_message, session_id)

    return jsonify({"reply": response_message})

@app.route('/sessions', methods=['GET'])
def get_sessions():
    """
    Endpoint to retrieve all session IDs from the database.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM conversation ORDER BY MAX(timestamp) DESC")
        sessions = cursor.fetchall()
        session_ids = [row[0] for row in sessions]
        return jsonify({"sessions": session_ids})
    except Exception as e:
        logging.error(f"Error fetching session IDs: {e}")
        return jsonify({"error": "Unable to fetch session IDs."}), 500

from manipulator import generate_manipulative_response

@app.route("/manipulate", methods=["POST"])
def manipulate():
    """
    Endpoint to simulate manipulative agent responses.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Generate manipulative response
    manipulative_response = generate_manipulative_response(user_message)

    return jsonify({"reply": manipulative_response})

from feedback_analyzer import analyze_response

@app.route("/analyze-feedback", methods=["POST"])
def analyze_feedback():
    """
    Endpoint to analyze user responses and provide feedback.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Analyze the user's response
    feedback = analyze_response(user_message)

    return jsonify({"feedback": feedback})

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ("name", "email", "message")):
            return jsonify({"error": "Missing required fields: name, email, message"}), 400

        name = data["name"]
        email = data["email"]
        message = data["message"]

        SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
        EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME", "")
        EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
        EMAIL_FROM = os.environ.get("EMAIL_FROM", EMAIL_USERNAME)

        missing = [k for k, v in {
            "EMAIL_USERNAME": EMAIL_USERNAME,
            "EMAIL_PASSWORD": EMAIL_PASSWORD,
            "EMAIL_FROM": EMAIL_FROM
        }.items() if not v]

        if missing:
            return jsonify({"error": f"Email service not configured on server (missing: {', '.join(missing)})"}), 500

        subject = f"New message from {name}"
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_USERNAME
        msg["Subject"] = subject
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_USERNAME, msg.as_string())

        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

# ---- Main ---- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
