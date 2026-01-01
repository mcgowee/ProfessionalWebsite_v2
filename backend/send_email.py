from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuration (update these settings for your environment)
SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
SMTP_PORT = 587
EMAIL_USERNAME = "mcgowee@gmail.com"  # Replace with your email address
EMAIL_PASSWORD = "K8%W2J#MsX!Zgg"    # Replace with your email password
EMAIL_FROM = "your-email@example.com"     # Replace with the sender's email

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        # Parse JSON request
        data = request.get_json()
        if not data or not all(key in data for key in ("name", "email", "message")):
            return jsonify({"error": "Missing required fields: name, email, message"}), 400

        name = data["name"]
        email = data["email"]
        message = data["message"]

        # Create email content
        subject = f"New message from {name}"
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_USERNAME  # Send to your inbox
        msg["Subject"] = subject
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_USERNAME, msg.as_string())

        # Return success response
        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
