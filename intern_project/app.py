from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get sensitive data from environment variables
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')


print(f"Sender Email: {sender_email}")
print(f"Sender Password: {sender_password}")
# Function to send email

def send_email(receiver_email, amount, payment_method):
    subject = "Payment Confirmation"
    body = f'''\n Dear user,\n\nYour payment of ₹{amount} via {payment_method} 
    has been received.\n\nYour generosity is a vital part of our success. 
    Thank you for believing in our cause!!
    \n\nBest regards,\nKindness Vault Foundation'''

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish a secure session with Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # Terminate the SMTP session
        server.quit()


# Flask route for form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        amount = request.form['amt']
        payment_method = request.form.get('payment_method')  # Use .get() to avoid KeyError

        # Send email to the user
        send_email(email, amount, payment_method)

        return f"Thank you for your kindness and support."

    return render_template('payment_form.html')


if __name__ == "__main__":
    app.run(debug=True)
