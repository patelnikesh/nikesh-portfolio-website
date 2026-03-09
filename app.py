from flask import Flask, request, render_template
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Load secure environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = EmailMessage()
        msg['Subject'] = f'New message from {name}'
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER

        msg.set_content(
            f"New Contact Form Message\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )

        # Gmail SMTP Server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return "Email sent successfully!"

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # configurable host/port/debug via environment; keep use_reloader=False to avoid duplicate side-effects
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "1").lower() in ("1", "true", "yes")
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)
