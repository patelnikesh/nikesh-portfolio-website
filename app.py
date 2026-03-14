from flask import Flask, request, render_template, abort, jsonify
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import logging
import os

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not EMAIL_USER or not EMAIL_PASS:
    raise RuntimeError("EMAIL_USER and EMAIL_PASS environment variables must be set.")

def validate_input(name, email, message):
    if not name or not email or not message:
        abort(400, "All fields are required.")
    if len(name) > 100:
        abort(400, "Name too long.")
    if len(message) > 5000:
        abort(400, "Message too long.")
    if "@" not in email or "." not in email.split("@")[-1]:
        abort(400, "Invalid email address.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    logger.info(f"Form submitted — name: {name}, email: {email}")
    validate_input(name, email, message)

    try:
        msg = EmailMessage()
        msg['Subject']  = f'New Contact Form Message from {name}'
        msg['From']     = EMAIL_USER
        msg['To']       = EMAIL_USER
        msg['Reply-To'] = email
        msg.set_content(
            f"New Contact Form Message\n\n"
            f"Name:    {name}\n"
            f"Email:   {email}\n\n"
            f"Message:\n{message}"
        )

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        logger.info("Email sent successfully.")
        return jsonify({"status": "success", "message": "Email sent successfully!", "color": "green"})

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {e}")
        return jsonify({"status": "error", "message": "Authentication error."}), 500

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return jsonify({"status": "error", "message": "SMTP error."}), 500

    except Exception as e:
        logger.exception("Unexpected error.")
        return jsonify({"status": "error", "message": "Something went wrong."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="127.0.0.1", port=port)
