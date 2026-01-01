import eventlet
# Crucial: Patch socket for Flask-SocketIO, but skip thread for Azure SDK
eventlet.monkey_patch(thread=False, socket=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ NEW: Socket.IO
from flask_socketio import SocketIO

# Configure logging
logging.basicConfig(
    filename="test_chatbot.log",  # Log file name
    level=logging.DEBUG,          # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)

from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)

# Keep CORS permissive on the API (you can tighten later)
CORS(app)

# ✅ NEW: SocketIO attached to this Flask app at import time (required for gunicorn)
# IMPORTANT: cors_allowed_origins="*" is fine behind nginx; tighten later if desired.
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
    # async_mode='eventlet' is default if installed, which is what we want
)

# If you want to keep your old commented CORS allowlist, it's fine to keep it commented:
# CORS(app, resources={r"/*": {"origins": ["https://sakuraai.cloud", "https://www.sakuraai.cloud", "https://sakuraai.org", "https://www.sakuraai.org"]}})

SECRET_API_KEY = os.environ.get("FLASK_API_KEY")  # None if not set

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    logging.error(f"Unhandled Exception: {str(e)}\n{traceback.format_exc()}")
    return jsonify({
        "error": "Internal Server Error (Captured)", 
        "message": str(e),
        "trace": traceback.format_exc()
    }), 500




@app.get("/health")
def health():
    return jsonify({"ok": True})


def require_api_key():
    """
    If FLASK_API_KEY is set, require Authorization: Bearer <key>.
    If not set, allow requests (useful for dev; still keep server private).
    """
    if not SECRET_API_KEY:
        return None  # dev mode / not configured

    api_key = request.headers.get("Authorization", "")
    if api_key != f"Bearer {SECRET_API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    return None


# ---- Wordle Code (Unchanged) ---- #
@app.route("/api/solve", methods=["POST"])
def solve():
    """
    Wordle Solver endpoint: processes guesses and feedback to suggest words.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    from wordle_solver import process_wordle_request

    data = request.get_json(silent=True) or {}

    return process_wordle_request(data)


# ---- Chatbot Code ---- #
@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Chatbot endpoint: accepts user input, processes it, and returns a response.
    """
    # Validate the API key
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    user_message = data.get("message", "")

    if not session_id:
        return jsonify({"error": "Session ID is required."}), 400

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    from chatbot import process_message

    # Call the chatbot logic
    response_message = process_message(user_message, session_id)

    return jsonify({"reply": response_message})


@app.route("/api/manipulate", methods=["POST"])
def manipulate():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    from manipulator import generate_manipulative_response  # lazy import
    manipulative_response = generate_manipulative_response(user_message)

    return jsonify({"reply": manipulative_response})


@app.route("/api/analyze-feedback", methods=["POST"])
def analyze_feedback():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    from feedback_analyzer import analyze_response  # lazy import
    feedback = analyze_response(user_message)

    return jsonify({"feedback": feedback})


@app.route("/api/send-email", methods=["POST"])
@app.route("/api/contact", methods=["POST"])
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


@app.route("/api/generate", methods=["POST"])
def generate():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}

    # Accept either {prompt: "..."} or {message: "..."}
    prompt = (data.get("prompt") or data.get("message") or "").strip()
    session_id = data.get("session_id") or "default-session"

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    from chatbot import process_message  # lazy import
    response_message = process_message(prompt, session_id)

    return jsonify({
        "generated_text": response_message,
        "reply": response_message,          # compatibility for clients expecting "reply"
        "session_id": session_id
    })


@app.route("/api/sql_qa", methods=["POST"])
def sql_qa_route():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    question = (data.get("question") or data.get("prompt") or "").strip()
    session_id = data.get("session_id") or "default-sql-session"
    max_rows = int(data.get("max_rows") or 50)

    if not question:
        return jsonify({"error": "Missing question"}), 400

    try:
        from sql_qa import sql_qa
        # TEST: Just import to verify
        # return jsonify({"status": "SQL QA Imported OK"}) 

        result = sql_qa(question=question, session_id=session_id, max_rows=max_rows)
        if "error" in result:
             return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        # Bare bones error handling to avoid crashing the handler
        return jsonify({"error": f"Crash in SQL QA: {str(e)}"}), 500


# ✅ NEW: Register your live translation namespace (ONLY file you have: services/azure_live_ws.py)
# This must happen after socketio is created.
try:
    from services.azure_live_ws import AzureLiveNamespace
    socketio.on_namespace(AzureLiveNamespace("/azure-live"))
    logging.info("Registered AzureLiveNamespace at /azure-live")
except Exception as e:
    logging.exception("Failed to register AzureLiveNamespace: %s", e)


# ---- Main ---- #
# For local dev only. In production you run gunicorn via systemd (as you already do).
if __name__ == "__main__":
    # If you ever run directly, use socketio.run so /socket.io works
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
