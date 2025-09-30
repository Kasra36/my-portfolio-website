from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SUPER_SECRET_KEY = os.getenv("SUPER_SECRET_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = SUPER_SECRET_KEY

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message_content = request.form.get('message')
        
        if not message_content:
            flash('Message cannot be empty', 'error')
            return redirect(url_for('contact'))
        
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = EMAIL_USER
            msg['Subject'] = 'Portfolio Website User Message'
            body = f"Message from: {request.form.get('email')}\n\n{message_content}"
            msg.attach(MIMEText(body, 'plain'))
        

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())

            flash('Message sent successfully!', 'success')
            return redirect(url_for('home'))
        
        except Exception as e:
            print(e)
            flash('Failed to send message', 'error')
            return redirect(url_for('home'))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)