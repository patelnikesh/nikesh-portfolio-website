from flask import Flask, request, render_template, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# It is highly recommended to set these in the Render "Environment" tab
# instead of writing them directly in the code.
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get data from form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not EMAIL_USER or not EMAIL_PASS:
            return jsonify({"status": "error", "message": "Server configuration missing (API Keys)"}), 500

        msg = EmailMessage()
        msg['Subject'] = f'New message from {name}'
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER # You receive the email

        msg.set_content(
            f"New Contact Form Message\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )

        # Gmail SMTP Server Connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200

    except Exception as e:
        print(f"Deployment Error: {str(e)}") # This will show in Render Logs
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Render uses the PORT environment variable. 
    # We must use 0.0.0.0 to allow external traffic.
    PORT = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
